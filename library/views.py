from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from accounts.models import User
from django.views.generic import ListView
from library.models import Book, Signout
from library.tasks import send_email_reminders
from library.utils import sign_back_all_borrows
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone

class BooksView(LoginRequiredMixin, ListView):
    model = Book

    def get_queryset(self, *args, **kwargs):
        qs = super(BooksView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("unique_number")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            active = Signout.objects.filter(user=self.request.user, signed_back_in=False).select_related('book')
            context['user_active_ids'] = set(s.book_id for s in active)
            context['user_borrow_count'] = len(context['user_active_ids'])
        else:
            context['user_active_ids'] = set()
            context['user_borrow_count'] = 0
        return context


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, book_id, *args, **kwargs):
        book = get_object_or_404(Book, id=book_id)
        active = Signout.objects.filter(user=request.user, signed_back_in=False)
        active_ids = set(s.book_id for s in active)

        if book.available_copies <= 0 or book.id in active_ids or len(active_ids) >= 3:
            return redirect('books')

        now = timezone.now()
        expected_return_date = now + timedelta(days=21)
        Signout.objects.create(
            book=book,
            user=request.user,
            signout_date=now,
            signin_date=None,
            expected_return_date=expected_return_date,
        )
        book.available_copies -= 1
        book.save()
        return redirect('/?msg=checked_out')


class MyBorrowsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        now = timezone.now()
        signouts = (
            Signout.objects.filter(user=request.user, signed_back_in=False)
            .select_related('book')
            .order_by('expected_return_date')
        )
        for s in signouts:
            s.is_overdue = s.expected_return_date < now
        context = {'signouts': signouts}
        return render(request, "signin.html", context)


class ReturnView(LoginRequiredMixin, View):
    def post(self, request, signout_id, *args, **kwargs):
        signout = get_object_or_404(Signout, id=signout_id)
        if signout.user != request.user:
            return HttpResponseForbidden()
        signout.signed_back_in = True
        signout.signin_date = timezone.now()
        signout.save()
        signout.book.available_copies += 1
        signout.book.save()
        return redirect('signin')
    

class AddBookView(UserPassesTestMixin, View):    
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        context = {"error": False}
        return render(request, "add_book.html", context)

    def post(self, request, *args, **kwargs):
        errors = []
        book_number = request.POST.get('book_number')
        title = request.POST.get('title')
        creators = request.POST.get('creators')
        description = request.POST.get('description')
        publisher = request.POST.get('publisher')
        publish_date = request.POST.get('publish_date')
        total_copies = int(request.POST.get('total_copies') or 1)

        if title == '':
            errors.append("Title is Empty!")
            title = None

        try:
            book = Book(title=title, creators=creators, description=description, publisher=publisher,
                        publish_date=publish_date, total_copies=total_copies, available_copies=total_copies,
                        unique_number=book_number)
            book.save()
        except:
            errors.append("Book number is not unique!")
            
        context = {"error": (len(errors) > 0), "errors": errors, "book": book}
        return render(request, "add_book.html", context)


class SignoutsHistoryView(UserPassesTestMixin, ListView):    
    model = Signout
    template_name: str = "signouts_history.html"
    def get_queryset(self, *args, **kwargs):
        qs = super(SignoutsHistoryView, self).get_queryset(*args, **kwargs)
        return qs.filter(signed_back_in=False)

    def test_func(self):
        return self.request.user.is_superuser

class OverdueView(UserPassesTestMixin, ListView):    
    model = Signout
    template_name: str = "signouts_history.html"
    def get_queryset(self, *args, **kwargs):
        qs = super(OverdueView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(signed_back_in=False)
        return qs.filter(expected_return_date__lt=datetime.now())

    def test_func(self):
        return self.request.user.is_superuser

class SendEmailsView(View):

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword")

        if keyword != "alwayshalalmemes":
            res =  HttpResponse("Something went wrong.")
            res.status_code = 500
            return res

        try:
            send_email_reminders()
        except:
            res =  HttpResponse("Something went wrong.")
            res.status_code = 500
            return res

        return HttpResponse("Success.")

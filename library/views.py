from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic.base import View
from accounts.models import User
from django.views.generic import ListView
from library.models import Book, Signout
from library.tasks import send_email_reminders
from library.utils import sign_back_all_borrows
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse

class SignoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {"error": False}
        return render(request, "signout.html", context)

    def post(self, request, *args, **kwargs):
        error = False
        book_number = request.POST.get('book_number')

        try:
            book = Book.objects.get(unique_number=book_number)
        except Book.DoesNotExist:
            error = True
            
        if error:
            context = {"error": True}
            return render(request, "signout.html", context)
        # if already unavailable, assuming the person returned and didn't sign it in
        if not book.available:
            sign_back_all_borrows(book)

        user = User.objects.get(id=request.user.id)
        signout_time = datetime.now()
        expected_return_date = signout_time + timedelta(days=21)
        signout = Signout(book=book, user=user, signout_date=signout_time, signin_date=None, expected_return_date=expected_return_date)
        signout.save()
        book.available = False
        book.save()
        context = {"book_number": book_number, "book": book, "success": True}
        return render(request, "signout.html", context)
    
class SigninView(View):
    def get(self, request, *args, **kwargs):
        context = {"error": False}
        return render(request, "signin.html", context)

    def post(self, request, *args, **kwargs):
        error = False
        book_number = request.POST.get('book_number')
        
        try:
            book = Book.objects.get(unique_number=book_number)
        except Book.DoesNotExist:
            error = True
            
        if error:
            context = {"error": True}
            return render(request, "signin.html", context)

        sign_back_all_borrows(book)

        book.available = True
        book.save()
        
        context = {"book_number": book_number, "book": book, "success": True}
        return render(request, "signin.html", context)

class BooksView(ListView):
    model = Book

    def get_queryset(self, *args, **kwargs):
        qs = super(BooksView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("unique_number")
        return qs
    

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
        author = request.POST.get('author')
        description = request.POST.get('description')
        available = True if request.POST.get('available') == 'on' else False

        if title == '':
            errors.append("Title is Empty!")
            title = None

        try:
            book = Book(title=title, author=author, description=description, available=available, unique_number=book_number)
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

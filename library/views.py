from datetime import datetime
from distutils import errors
from django.shortcuts import render
from django.views.generic.base import View
from accounts.models import User
from django.views.generic import ListView
from library.models import Books, Signouts
from library.utils import sign_back_all_borrows

class SignoutView(View):
    def get(self, request, *args, **kwargs):
        context = {"error": False}
        return render(request, "signout.html", context)

    def post(self, request, *args, **kwargs):
        error = False
        book_number = request.POST.get('book_number')

        try:
            book = Books.objects.get(unique_number=book_number)
            print(book.title)
        except Books.DoesNotExist:
            error = True
            
        if error:
            context = {"error": True}
            return render(request, "signout.html", context)
        # if already unavailable, assuming the person returned and didn't sign it in
        if not book.available:
            sign_back_all_borrows(book)

        user = User.objects.get(id=request.user.id)
        signout_time = datetime.now()
        signout = Signouts(book=book, user=user, signout_date=signout_time, signin_date=None)
        signout.save()
        book.available = False
        book.save()
        context = {"book_number": book_number, "book": book}
        return render(request, "signout_success.html", context)
    
class SigninView(View):
    def get(self, request, *args, **kwargs):
        context = {"error": False}
        return render(request, "signin.html", context)

    def post(self, request, *args, **kwargs):
        error = False
        book_number = request.POST.get('book_number')
        
        try:
            book = Books.objects.get(unique_number=book_number)
            print(book.title)
        except Books.DoesNotExist:
            error = True
            
        if error:
            context = {"error": True}
            return render(request, "signin.html", context)

        sign_back_all_borrows(book)

        book.available = True
        book.save()
        
        context = {"book_number": book_number, "book": book}
        return render(request, "return_success.html", context)

class BooksView(ListView):
    model = Books

    def get_queryset(self, *args, **kwargs):
        qs = super(BooksView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("unique_number")
        return qs
    

class AddBookView(View):    
    def get(self, request, *args, **kwargs):
        context = {"error": False}
        return render(request, "add_book.html", context)

    def post(self, request, *args, **kwargs):
        errors = []
        print(request.POST)

        book_number = request.POST.get('book_number')
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        available = True if request.POST.get('available') == 'on' else False

        if title == '':
            errors.append("Title is Empty!")
            title = None

        try:
            book = Books(title=title, author=author, description=description, available=available, unique_number=book_number)
            book.save()
        except:
            errors.append("Book number is not unique!")
            
        context = {"error": (len(errors) > 0), "errors": errors, "book": book}
        return render(request, "add_book.html", context)


class SignoutsHistoryView(ListView):    
    model = Signouts
    template_name: str = "signouts_history.html"
    def get_queryset(self, *args, **kwargs):
        return super(SignoutsHistoryView, self).get_queryset(*args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     signouts = 
    #     context = {"error": False}
    #     return render(request, "signouts_history.html", context)
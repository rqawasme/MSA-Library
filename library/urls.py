from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignoutView.as_view(), name='home'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('addbook/', views.AddBookView.as_view(), name='addbook'),
    path('history/', views.SignoutsHistoryView.as_view(), name='history'),
]
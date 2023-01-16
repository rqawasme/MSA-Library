from django.urls import path
from django.conf.urls import include
from library.api.views import BookViewSet, SignoutViewSet
from . import views
from rest_framework import routers
 
# define the router
router = routers.DefaultRouter()
 
# define the router path and viewset to be used
router.register(r'booklist', BookViewSet)
router.register(r'signoutlist', SignoutViewSet)

urlpatterns = [
    path('', views.SignoutView.as_view(), name='home'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('addbook/', views.AddBookView.as_view(), name='addbook'),
    path('history/', views.SignoutsHistoryView.as_view(), name='history'),
    path('overdue/', views.OverdueView.as_view(), name='overdue'),
    path('sendreminders/', views.SendEmailsView.as_view()),
    # REST API
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
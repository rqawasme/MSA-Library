from library.models import Book, Signout
from rest_framework import viewsets
from .serializers import BookSerializer, SignoutSerializer
 
# create a viewset
class BookViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Book.objects.all()
     
    # specify serializer to be used
    serializer_class = BookSerializer

class SignoutViewSet(viewsets.ModelViewSet):
    queryset = Signout.objects.all()
    serializer = SignoutSerializer(queryset, many=True)


from rest_framework import serializers
from ..models import Book, Signout

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'description', 'creators', 'publisher', 'publish_date', 'total_copies', 'available_copies', 'unique_number')

class SignoutSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Signout
        fields = ('book', 'user', 'signout_date', 'signed_back_in', 'signin_date')
from django.db import models
from accounts.models import User

class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    creators = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    publish_date = models.CharField(max_length=100, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    isbn = models.CharField(max_length=20, blank=True)
    unique_number = models.IntegerField(unique=True, blank=False)


class Signout(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    signout_date = models.DateTimeField(blank=False)
    signin_date = models.DateTimeField(default=None, null=True, blank=True)
    signed_back_in = models.BooleanField(default=False)
    expected_return_date = models.DateTimeField(default=None, null=True, blank=True)

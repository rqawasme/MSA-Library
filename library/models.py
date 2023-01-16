from django.db import models
from accounts.models import User

class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True, blank=False)
    # image = models.ImageField()
    unique_number = models.IntegerField(unique=True, blank=False)


class Signout(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    signout_date = models.DateTimeField(blank=False)
    signin_date = models.DateTimeField(default=None, null=True, blank=True)
    signed_back_in = models.BooleanField(default=False)
    expected_return_date = models.DateTimeField(default=None, null=True, blank=True)

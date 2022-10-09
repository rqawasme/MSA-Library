from datetime import datetime
from library.models import Book, Signout

def sign_back_all_borrows(book: Book):
    signouts = Signout.objects.filter(book=book, signed_back_in=False)
    for signout in signouts:
        signout.signed_back_in = True
        signout.signin_date = datetime.now()
        signout.save()
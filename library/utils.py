from datetime import datetime
from library.models import Books, Signouts

def sign_back_all_borrows(book: Books):
    signouts = Signouts.objects.filter(book=book, signed_back_in=False)
    for signout in signouts:
        signout.signed_back_in = True
        signout.signin_date = datetime.now()
        signout.save()
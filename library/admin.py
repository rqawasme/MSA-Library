from django.contrib import admin

from library.models import Book, Signout

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'description', 'author', 'available', 'unique_number']
    
@admin.register(Signout)
class SignoutAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Signout._meta.get_fields()]
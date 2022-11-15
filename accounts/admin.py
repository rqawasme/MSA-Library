from django.contrib import admin

from accounts.models import User

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff']
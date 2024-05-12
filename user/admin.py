from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from authname.forms import UserForm, CustomUserChangeForm
# Register your models here.


# ModelAdmin

class CustomUserAdmin(UserAdmin):
    add_form = UserForm
    form = CustomUserChangeForm
    model = User
    add_fieldsets = (
        ('Personal Details', {'fields': ('email', 'full_name', 'username', 'picture', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Optinal',{'fields': ('bio','website')}),
       )
    fieldsets = (
        ('Personal Details', {'fields': ('email', 'full_name', 'username', 'picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Optinal',{'fields': ('bio','website')}),
        )


admin.site.register(User, CustomUserAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets +(
        (None,{'fields':('picture','phone','role')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('picture','phone','role')}),
    )

    list_display = ['username','email','first_name','last_name','role','is_staff']
    list_filter = ['role','is_staff']

admin.site.register(CustomUser,CustomUserAdmin)
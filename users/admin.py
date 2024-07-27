from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.utils.html import format_html


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    # readonly_fields = ('email', 'first_name', 'last_name', 'last_login', 'username', 'password', 'phone_number', 'is_superuser', 'is_admin', 'is_staff', 'is_superadmin', 'date_joined', 'is_active')
    ordering = ('-date_joined',)
    list_per_page = 5

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)

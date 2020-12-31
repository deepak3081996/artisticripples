from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
User = get_user_model()

class AccountAdmin(UserAdmin):
    
    list_display = ['username', 'email' , 'first_name', 'last_name', 'edit',]  # Contain only fields in your `custom-user-model`
    list_display_links = ('edit', 'email', )
    list_filter = ()  # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    search_fields = ['email', 'username']  # Contain only fields in your `custom-user-model` intended for searching
    ordering = ['email' , 'first_name', 'last_name' ,'username']  # Contain only fields in your `custom-user-model` intended to ordering
    filter_horizontal = () # Leave it empty. You have neither `groups` or `user_permissions`
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff','is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    class Meta:
        model = Account

admin.site.register(Account, AccountAdmin)

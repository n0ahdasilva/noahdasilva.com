from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, AuditEntry


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': (
            'password',
            'otp_secret', 
            'email',
            'username', 
            'full_name', 
            'date_joined', 
            'last_login', 
            'previous_login',
            'failed_login_attempts',
            'previous_failed_login_attempts',
            'original_email',
        )}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'is_superadmin',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            }
        ),
    )

    list_display = (
        'email', 
        'username', 
        'full_name', 
        'is_staff', 
        'last_login', 
        'date_joined'
    )
    list_filter = (
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'is_superadmin', 
        'groups'
    )
    readonly_fields = (
        'otp_secret',
        'original_email', 
        'date_joined', 
        'previous_login', 
        'last_login', 
        'failed_login_attempts', 
        'previous_failed_login_attempts'
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)

@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip', 'time',]
    list_filter = ['action',]
    readonly_fields = ['time']
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser')
    search_fields = ('email', 'username')
    list_filter = ('sex', 'date_joined')
    readonly_fields = ('date_joined', 'last_login', 'id', 'password')
    fieldsets = (
        ('Login Credentials', {
            "fields": (
                'username', 'email', 'password'

            ),
        }),
        ('Personal Information', {
            "fields": (
                'first_name', 'last_name', 'dob', 'avatar', 'sex', 'phone_number'

            ),
        }),
        ('Advanced', {
            "classes": ('collapse',),
            "fields": (
                'id', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )


admin.site.site_header = 'CloSho Admin'
admin.site.site_title = 'CloSho Admin'
admin.site.index_title = 'Welcome'

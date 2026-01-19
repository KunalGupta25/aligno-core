from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'role', 'gender', 'is_verified')
    list_filter = ('role', 'gender', 'is_verified')
    search_fields = ('name', 'phone_number')

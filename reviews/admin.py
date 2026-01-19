from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ride', 'reviewer', 'reviewed_user', 'rating')
    list_filter = ('rating',)

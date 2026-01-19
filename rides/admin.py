from django.contrib import admin
from .models import Ride, RideJoinRequest

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'start_location',
        'destination',
        'creator',
        'status',
        'available_seats'
    )
    list_filter = ('status',)


@admin.register(RideJoinRequest)
class RideJoinRequestAdmin(admin.ModelAdmin):
    list_display = ('ride', 'user', 'status', 'created_at')
    list_filter = ('status',)

from django.db import models
from users.models import User

class Ride(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_rides'
    )

    start_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance_km = models.PositiveIntegerField()
    
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    participants = models.ManyToManyField(
        User,
        related_name='joined_rides',
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_location} → {self.destination} ({self.status})"
    
    def complete_ride(self, user):
        if self.status == 'completed':
            raise ValueError("Ride already completed")

        if user != self.creator and not self.participants.filter(id=user.id).exists():
            raise ValueError("User not allowed to complete this ride")

        self.status = 'completed'
        self.save()

    
class RideJoinRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='join_requests'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ride_join_requests'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ride', 'user')

    def __str__(self):
        return f"{self.user} → {self.ride} ({self.status})"
    
    def accept(self):
        if self.status != 'pending':
            raise ValueError("Request already processed")

        ride = self.ride

        if ride.status == 'completed':
            raise ValueError("Ride already completed")

        if ride.available_seats <= 0:
            raise ValueError("No seats available")

        # add rider to ride
        ride.participants.add(self.user)
        ride.available_seats -= 1

        if ride.status == 'created':
            ride.status = 'active'

        ride.save()

        self.status = 'accepted'
        self.save()

    def reject(self):
        if self.status != 'pending':
            raise ValueError("Request already processed")

        self.status = 'rejected'
        self.save()



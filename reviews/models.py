from django.db import models
from users.models import User
from rides.models import Ride

class Review(models.Model):
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )

    reviewed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )

    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ride', 'reviewer', 'reviewed_user')

    def __str__(self):
        return f"{self.reviewer} → {self.reviewed_user} ({self.rating})"

    def clean(self):
        if self.ride.status != 'completed':
            raise ValueError("Reviews allowed only after ride completion")

        if self.reviewer == self.reviewed_user:
            raise ValueError("User cannot review themselves")

        valid_users = [self.ride.creator] + list(self.ride.participants.all())
        if self.reviewer not in valid_users or self.reviewed_user not in valid_users:
            raise ValueError("Invalid review participants")

        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")

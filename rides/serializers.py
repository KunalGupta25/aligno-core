from rest_framework import serializers
from .models import Ride, RideJoinRequest

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'


class RideJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideJoinRequest
        fields = '__all__'

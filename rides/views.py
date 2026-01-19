from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ride, RideJoinRequest
from .serializers import RideSerializer, RideJoinRequestSerializer

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        ride = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = ride.creator.__class__.objects.get(id=user_id)
            ride.complete_ride(user)
            return Response({'status': 'ride completed'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class RideJoinRequestViewSet(viewsets.ModelViewSet):
    queryset = RideJoinRequest.objects.all()
    serializer_class = RideJoinRequestSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        req = self.get_object()
        try:
            req.accept()
            return Response({'status': 'request accepted'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

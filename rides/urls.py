from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideJoinRequestViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet)
router.register(r'ride-requests', RideJoinRequestViewSet)

urlpatterns = router.urls

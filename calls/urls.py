from rest_framework.routers import DefaultRouter
from .views import CallRequestViewSet

router = DefaultRouter()
router.register(r'', CallRequestViewSet)

urlpatterns = router.urls

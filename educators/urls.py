from rest_framework.routers import DefaultRouter
from .views import EducatorViewSet

router = DefaultRouter()
router.register(r'', EducatorViewSet)

urlpatterns = router.urls

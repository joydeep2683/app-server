from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EducatorViewSet, StudentViewSet, CallRequestViewSet

router = DefaultRouter()
router.register(r'educators', EducatorViewSet)
router.register(r'students', StudentViewSet)
router.register(r'call-requests', CallRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

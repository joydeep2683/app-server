from django.urls import path
from . import views

urlpatterns = [
    path('', views.AreaListCreateAPIView.as_view(), name='area-list-create'),
    path('bulk/', views.AreaBulkCreateAPIView.as_view(), name='area-bulk-create'),
    path('<int:pk>/', views.AreaRetrieveUpdateDestroyAPIView.as_view(), name='area-detail'),
]

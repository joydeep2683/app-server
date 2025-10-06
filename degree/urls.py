from django.urls import path
from . import views

urlpatterns = [
    path('', views.DegreeListCreateAPIView.as_view(), name='degree-list-create'),
    path('bulk/', views.DegreeBulkCreateAPIView.as_view(), name='degree-bulk-create'),
    path('<int:pk>/', views.DegreeRetrieveUpdateDestroyAPIView.as_view(), name='degree-detail'),
]

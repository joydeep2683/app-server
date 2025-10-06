from rest_framework import viewsets
from .models import CallRequest
from .serializers import CallRequestSerializer

class CallRequestViewSet(viewsets.ModelViewSet):
    queryset = CallRequest.objects.all()
    serializer_class = CallRequestSerializer

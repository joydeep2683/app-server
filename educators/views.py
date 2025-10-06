from rest_framework import viewsets
from .models import Educator
from .serializers import EducatorSerializer

class EducatorViewSet(viewsets.ModelViewSet):
    queryset = Educator.objects.all()
    serializer_class = EducatorSerializer

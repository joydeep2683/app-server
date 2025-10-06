from rest_framework import viewsets
from .models import Educator, Student, CallRequest
from .serializers import EducatorSerializer, StudentSerializer, CallRequestSerializer

class EducatorViewSet(viewsets.ModelViewSet):
    queryset = Educator.objects.all()
    serializer_class = EducatorSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CallRequestViewSet(viewsets.ModelViewSet):
    queryset = CallRequest.objects.all()
    serializer_class = CallRequestSerializer

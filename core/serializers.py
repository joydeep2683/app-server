from rest_framework import serializers
from .models import Educator, Student, CallRequest

class EducatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educator
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CallRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRequest
        fields = '__all__'

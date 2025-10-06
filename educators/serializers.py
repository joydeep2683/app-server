from rest_framework import serializers
from .models import Educator, EducatorLicense, Degree, EducatorDegree, Area, EducatorArea

class EducatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educator
        fields = '__all__'

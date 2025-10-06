from rest_framework import serializers
from .models import Degree


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ['id', 'name']


class DegreeBulkCreateSerializer(serializers.ListSerializer):
    child = DegreeSerializer()

    def create(self, validated_data):
        degrees = [Degree(**item) for item in validated_data]
        return Degree.objects.bulk_create(degrees)

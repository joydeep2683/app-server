from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']


class AreaBulkCreateSerializer(serializers.ListSerializer):
    child = AreaSerializer()

    def create(self, validated_data):
        areas = [Area(**item) for item in validated_data]
        return Area.objects.bulk_create(areas)

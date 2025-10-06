from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Area
from .serializers import AreaSerializer, AreaBulkCreateSerializer


class AreaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class AreaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class AreaBulkCreateAPIView(APIView):
    """Accepts a JSON array of areas to create in bulk.

    Request body example:
    [
      {"name": "Area 1"},
      {"name": "Area 2"}
    ]
    """

    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"detail": "Expected a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AreaBulkCreateSerializer(data=request.data)
        # ListSerializer requires many=True when validating
        serializer = AreaSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        # Create using bulk_create for efficiency
        areas = [Area(**item) for item in serializer.validated_data]
        created = Area.objects.bulk_create(areas)
        out = AreaSerializer(created, many=True)
        return Response(out.data, status=status.HTTP_201_CREATED)
# from django.shortcuts import render

# Create your views here.

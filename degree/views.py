from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Degree
from .serializers import DegreeSerializer


class DegreeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer


class DegreeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer


class DegreeBulkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"detail": "Expected a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DegreeSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        degrees = [Degree(**item) for item in serializer.validated_data]
        created = Degree.objects.bulk_create(degrees)
        out = DegreeSerializer(created, many=True)
        return Response(out.data, status=status.HTTP_201_CREATED)

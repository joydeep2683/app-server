from rest_framework import viewsets

class BaseModelViewSet(viewsets.ModelViewSet):
    """Base ViewSet for common settings"""
    pagination_class = None  # Can add default pagination

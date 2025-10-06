from django.db import models
from django.contrib.auth.models import User

from area.models import Area
from degree.models import Degree
from core.models import TimeStampedModel

class Educator(TimeStampedModel):
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_licensed = models.BooleanField(default=False)

    class Meta:
        db_table = 'educator'

class EducatorLicense(models.Model):
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE, related_name='licenses')
    registration_number = models.CharField(max_length=255, blank=True, null=True)
    issuing_authority = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'educator_license'

class EducatorDegree(models.Model):
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE, related_name='degrees')
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)

    class Meta:
        db_table = 'educator_degree'

class EducatorArea(models.Model):
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE, related_name='areas')
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    class Meta:
        db_table = 'educator_area'

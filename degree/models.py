from django.db import models

# Create your models here.
class Degree(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'degree'
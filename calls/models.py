from django.db import models
from educators.models import Educator
from students.models import Student

class CallRequest(models.Model):
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'call_requests'

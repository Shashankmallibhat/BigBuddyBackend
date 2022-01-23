from django.db import models
from teacher.models import ClassRoom

# Create your models here.

class StudentClasses(models.Model):
    email = models.EmailField()
    usercode = models.CharField(max_length=50,null=True)
    classCode = models.CharField(max_length=50)
    
    
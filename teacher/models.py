from django.db import models

# Create your models here.

class ClassRoom(models.Model):
    className = models.CharField(max_length=50)
    teacherName = models.CharField(max_length=50)
    classCode = models.CharField(null=False,primary_key=True,max_length=50)
    usercode = models.CharField(max_length=50, null=False)
    videoStreamURL = models.URLField(default=None,null=True)
    classAvatarURL = models.URLField(default=None,null=True)
    studentList = models.TextField(default=None,null=True)

class ClassNotes(models.Model):
    classCode = models.ForeignKey(ClassRoom,on_delete = models.CASCADE,related_name='ClassCode')
    usercode = models.CharField(max_length=50)
    date = models.CharField(max_length=30,default=None)
    noteslink = models.URLField()
    
class ClassRecordings(models.Model):
    classCode = models.ForeignKey(ClassRoom,on_delete = models.CASCADE,related_name='Class_Code')
    usercode = models.CharField(max_length=50)
    date = models.CharField(max_length=30,default=None)
    recordinglink = models.URLField()
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin


# Create your models here.


class User_manager(BaseUserManager):
    def create_user(self, username, email, password, role,usercode):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role = role,usercode=usercode)
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self, username, email, password, role,usercode=None):
        user = self.create_user(username=username, email=email,password=password, role = role,usercode=usercode)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractUser,PermissionsMixin):
    class RoleChoices(models.TextChoices):
        Teacher = 'Teacher'
        Student = 'Student'
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(choices=RoleChoices.choices, max_length=20)
    password = models.CharField(max_length=50)
    usercode = models.CharField(max_length=50,default=None,editable=False)
    objects = User_manager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    def __str__(self):
        return self.username
    
    
class ProfileData(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    role = models.CharField(max_length=20)
    avatarURL = models.URLField(default=None)
    description = models.TextField(default=None)    
    
    def __str__(self):
        return self.username
    
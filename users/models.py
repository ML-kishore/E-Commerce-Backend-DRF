from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    ROLES_CHOICES = (('admin','ADMIN'),('user','USER'))

    role = models.CharField(max_length=5,choices=ROLES_CHOICES,default='user')
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True,max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username 
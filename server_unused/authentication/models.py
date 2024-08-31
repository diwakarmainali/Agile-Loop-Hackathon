from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import UsersManager

# Create your models here.
class UserAccount(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(("Name"), max_length=100)
    email=models.EmailField(("Email"), max_length=254,unique=True)
    is_active=models.BooleanField(("Is Active"), default=True)
    is_staff=models.BooleanField(("Is Staff"), default=False)
    user_points = models.IntegerField(default=0)
    
    USERNAME_FIELD = 'email'
    objects = UsersManager()
    

    def __str__(self):
        return self.email
    
    
    

    
    
    
    
    


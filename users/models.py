from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MaxValueValidator
from datetime import date

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=False, unique=True)
    photo = models.ImageField(default='user.png', upload_to='users/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, validators=[MaxValueValidator(date.today())])
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self) -> str:
        return self.username
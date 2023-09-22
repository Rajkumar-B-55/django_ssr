from django.db import models
from django.contrib.auth.models import AbstractUser


# alphabets_only = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabet characters are allowed')

class User(AbstractUser):
    role_choices = (
        ('admin', 'Admin'),
        ('user', 'User')
    )
    username = models.CharField(max_length=100, unique=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=100, choices=role_choices, default='user')
    phone_number = models.CharField(max_length=13, blank=True, null=True, unique=True)

    class Meta:
        db_table = 'tbl_users'

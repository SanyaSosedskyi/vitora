from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TYPE_CHOICES = (
        ('R', 'Reader'),
        ('B', 'Blogger')
    )
    user_type = models.CharField(max_length=1, choices=TYPE_CHOICES)


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='readers')
    is_adult = models.BooleanField(default=False)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='bloggers')
    birthday = models.DateField()
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)


class Interest(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    INTEREST_CHOICES = (
        ('Vh', 'Vehicles'),
        ('Hm', 'Humor'),
        ('Tr', 'Travel'),
        ('IT', 'IT'),
        ('Tc', 'Technologies')
    )
    interest = models.CharField(max_length=2, choices=INTEREST_CHOICES)

class Category(models.Model):
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    CATEGORY_CHOICES = (
        ('Vh', 'Vehicles'),
        ('Hm', 'Humor'),
        ('Tr', 'Travel'),
        ('IT', 'IT'),
        ('Tc', 'Technologies')
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)




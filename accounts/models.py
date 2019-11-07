from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver


class User(AbstractUser):
    TYPE_CHOICES = (
        ('R', 'Reader'),
        ('B', 'Blogger')
    )
    user_type = models.CharField(max_length=1, choices=TYPE_CHOICES)


class CategoryDictionary(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reader(models.Model):
    interest = models.ManyToManyField(CategoryDictionary, related_name='interested_readers')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='readers')
    is_adult = models.BooleanField(default=False)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='bloggers')
    birthday = models.DateField()
    category = models.ManyToManyField(CategoryDictionary, related_name='category_bloggers')
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)




from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.db import transaction

class ReaderSignUpForm(UserCreationForm):

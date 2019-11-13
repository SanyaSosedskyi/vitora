from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, Reader, Blogger, CategoryDictionary
from django.db import transaction
from .tasks import send_email_task

class ReaderSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    interests = forms.ModelMultipleChoiceField(
        queryset=CategoryDictionary.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    is_adult = forms.BooleanField(
        widget=forms.CheckboxInput,
    )


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 'R'
        email = self.cleaned_data.get('email')
        user.email = email
        user.save()
        send_email_task.delay(email)
        reader = Reader.objects.create(user=user, is_adult=self.cleaned_data.get('is_adult'))
        reader.interest.add(*self.cleaned_data.get('interests'))
        return user


YEAR_SELECT_CHOICES = list(range(1960,2009))


class BloggerSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    interests = forms.ModelMultipleChoiceField(
        queryset=CategoryDictionary.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_SELECT_CHOICES))
    country = forms.CharField(widget=forms.TextInput)
    city = forms.CharField(widget=forms.TextInput)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 'B'
        user.email = self.cleaned_data.get('email')
        user.save()
        email = self.cleaned_data.get('email')
        send_email_task.delay(email)
        blogger = Blogger.objects.create(user=user, birthday=self.cleaned_data.get('birthday'),
                                         country=self.cleaned_data.get('country'),
                                         city=self.cleaned_data.get('city'))
        blogger.category.add(*self.cleaned_data.get('interests'))
        return user

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from accounts.forms import ReaderSignUpForm, BloggerSignUpForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from accounts.models import Reader, Blogger, User
from django.http import JsonResponse
from django.contrib.auth.forms import  AuthenticationForm
from django.conf import settings
import urllib.parse
import urllib.request
import json
from django.contrib import messages


def signup(request):
    return render(request, 'signup.html')


class LoginViewCustom(LoginView):
    template_name = 'login.html'
    model = User

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(self.request, user)
                return redirect('home')
            else:
                messages.error(self.request, 'Incorrect username or password. Please try again.')
                return render(self.request, 'login.html', {'form': form})
        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return render(self.request, 'login.html', {'form': form})


class BloggerSignUpView(CreateView):
    model = Blogger
    form_class = BloggerSignUpForm
    template_name = 'blogger_signup.html'

    def get_contex_data(self, **kwargs):
        kwargs['user_type'] = 'blogger'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            user = form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return render(self.request, 'blogger_signup.html', {'form': form})


class ReaderSignUpView(CreateView):
    model = Reader
    form_class = ReaderSignUpForm
    template_name = 'reader_signup.html'

    def get_contex_data(self, **kwargs):
        kwargs['user_type'] = 'reader'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            user = form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return render(self.request, 'reader_signup.html', {'form': form})


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

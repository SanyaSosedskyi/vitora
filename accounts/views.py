from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.views.generic import CreateView
from accounts.models import Reader, Blogger


def signup(request):
    return render(request, 'signup.html')


def blogger_signup(CreateView):
    model = Blogger
    form_class = BloggerSignUpForm
    template_name = 'blogger_signup.html'

    def get_contex_data(self, **kwargs):
        kwargs['user_type'] = 'blogger'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def reader_signup(CreateView):
    model = Reader
    form_class = ReaderSignUpForm
    template_name = 'reader_signup.html'

    def get_contex_data(self, **kwargs):
        kwargs['user_type'] = 'reader'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')



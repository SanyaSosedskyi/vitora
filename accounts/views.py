from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import ReaderSignUpForm, BloggerSignUpForm
from django.views.generic import CreateView
from accounts.models import Reader, Blogger, User
from django.http import JsonResponse

def signup(request):
    return render(request, 'signup.html')


class BloggerSignUpView(CreateView):
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


class ReaderSignUpView(CreateView):
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


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

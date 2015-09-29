from django.shortcuts import render, redirect
from django.contrib.auth import (login as auth_login, logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.utils.http import is_safe_url
from django.conf import settings

from .models import DemoUser
from .forms import LoginForm

# Create your views here.

@require_GET
def base(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        return redirect('login')


@require_GET
@login_required
def home(request):
    return render(request, 'base.html')


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if not redirect_to or not is_safe_url(url=redirect_to, host = request.get_host()):
                redirect_to = settings.LOGIN_REDIRECT_URL
            return redirect(redirect_to)
    else:
        form = LoginForm()

    context = {'form' : form, 'next' : redirect_to}
    return render(request, 'authentication/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect(settings.LOGIN_URL)


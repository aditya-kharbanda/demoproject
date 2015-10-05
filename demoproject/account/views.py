from django.shortcuts import render, redirect
from django.contrib.auth import (login as auth_login, logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

from .models import DemoUser
from .forms import LoginForm, ForgotPasswordForm, ResetPasswordForm, UserCreationForm, SearchUserForm

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


@require_http_methods(['GET', 'POST'])
def forgot_password(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            opts = {
                    'token_generator' : default_token_generator,
                    'from_email' : settings.DEFAULT_FROM_EMAIL,
                    'email_template_name' : 'email/password_reset/password_reset_email_text.txt',
                    'subject_template_name' : 'email/password_reset/password_reset_subject.txt',
                    'request' : request,
                    'html_email_template_name' : None
            }
            form.save(**opts)
            return render(request, 'authentication/password_reset_email_sent.html')
    else:
        form = ForgotPasswordForm()
    context = {'form' : form}
    return render(request, 'authentication/password_reset_form.html', context)


@require_http_methods(['GET', 'POST'])
@sensitive_post_parameters()
@never_cache
def reset_password(request, uidb64=None, token=None):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    assert uidb64 is not None and token is not None

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = DemoUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = ResetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'authentication/password_reset_complete.html')
        else:
            form = ResetPasswordForm(user)
    else:
        validlink = False
        form = None
    context = { 'validlink' : validlink, 'form' : form }
    return render(request, 'authentication/password_reset_confirm_form.html', context)

@require_GET
@login_required
def search(request):
    context = { 'form' : SearchUserForm }
    return render(request, 'search/search_base.html', context);

@require_GET
@login_required
def search_users(request):
    name = request.GET.get('name')
    data = []
    if name:
        users = DemoUser.objects.filter(first_name__icontains = name)
        print(users)
        data = [ { 'id' : user.id , 'name' : user.get_full_name()} for user in users ]
    print(data);
    return JsonResponse(data = {'users': data});




    




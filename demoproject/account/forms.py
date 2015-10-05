from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import DemoUser

class LoginForm(AuthenticationForm):
    pass

class UserCreationForm(forms.ModelForm):
    passwd1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    passwd2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, help_text = "Should be same as Password")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        for field in self.fields:
            self.fields[field].required = True

    def clean_passwd2(self):
        passwd1 = self.cleaned_data.get("passwd1")
        passwd2 = self.cleaned_data.get("passwd2")
        if passwd1 and passwd2 and passwd1 != passwd2:
            raise forms.ValidationError("Passwords don't match")
        return passwd2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data["passwd1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = DemoUser
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'dob', 'phone_number']

class ForgotPasswordForm(PasswordResetForm):
    def clean_email(self):
       email = self.cleaned_data.get('email')
       if email and DemoUser.objects.filter(email = email).count() == 0:
           raise forms.ValidationError("We cannot find account with this email. Please verify your email address and try again.")
       return email

class ResetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password2'].label = 'Confirm Password'

class SearchUserForm(forms.Form):
    name = forms.CharField()


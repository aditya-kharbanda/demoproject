from django.contrib import admin
from .models import DemoUser
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm  

# Register your models here.
class DemoUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'is_staff', 'phone_number')
    fieldsets = (
            ('None', {'fields' : (('username', 'email'), 'password')}),
            ('Personal Info', {'fields' : (('first_name', 'last_name'), ('gender', 'dob'),'phone_number', 'profile_pic')}),
            ('Permission', {
                'fields': (('is_staff', 'is_superuser', 'is_active'),'groups', 'user_permissions'),
                'classes': ('grp-collapse grp-closed',)
                }),
            ('Important Dates', {
                'fields': ('last_login', 'date_joined'),
                'classes': ('grp-collapse grp-closed',)
                })
    )
    add_fieldsets = (
            ('None', {
                'classes' : ('wide',),
                'fields': ('username', 'email', 'first_name', 'last_name', 'gender', 'dob', 'phone_number', 'passwd1', 'passwd2')
                }),)
    add_form = UserCreationForm
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

admin.site.register(DemoUser, DemoUserAdmin)

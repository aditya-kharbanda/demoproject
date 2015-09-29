from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

class DemoUser(AbstractUser):
    profile_pic = models.ImageField(upload_to = 'profile_pics/', blank = True)
    dob = models.DateField(blank =True, null = True)
    phone_number = PhoneNumberField(max_length = 15, unique = True)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, default = GENDER_CHOICES[0][0]);
    
    class Meta:
        unique_together = ('email',)
        verbose_name = 'User'


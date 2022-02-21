from email.policy import default
from faulthandler import disable
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name  , self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class contact(models.Model):
    first_name = User.first_name
    last_name = models.CharField(max_length = 50)
    email_address = models.EmailField(max_length = 150)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name ,self.user.email)

MARITAL_STATUS = (
    ('select','Select'),
    ('y', 'Yes'),
    ('n','No'),
)

GENDER_CHOICES = (
   ('M', 'Male'),
   ('F', 'Female')
)

loan_type = (
    ('Home_loan','Home Loan'),
    ('Car_loan', 'Car Loan'),
    ('Personal_loan','Personal Loan'),
)

class homeloan(models.Model):
    firstname = models.CharField(max_length=12, blank=False)
    lastname = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length = 150)
    phone_number = models.CharField(max_length=12, blank=True)
    income = models.IntegerField(blank=True,validators=[MinValueValidator(75000)])
    gender = models.CharField(max_length=1)
    MARITAL_STATUS = models.CharField(max_length=6)
    loan_type = models.CharField(max_length=13, default="Home_loan")


    def __str__(self):
        return self.title

class carloan(models.Model):
    firstname = models.CharField(max_length=12, blank=False)
    lastname = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length = 150)
    phone_number = models.CharField(max_length=12, blank=True)
    income = models.IntegerField(blank=True,validators=[MinValueValidator(25000)])
    gender = models.CharField(max_length=1)
    MARITAL_STATUS = models.CharField(max_length=6)
    loan_type = models.CharField(max_length=13,default="Car_loan")

    def __str__(self):
        return self.title


class personalloan(models.Model):
    firstname = models.CharField(max_length=12, blank=False)
    lastname = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length = 150)
    phone_number = models.CharField(max_length=12, blank=True)
    income = models.IntegerField(blank=True,validators=[MinValueValidator(20000)])
    gender = models.CharField(max_length=1)
    MARITAL_STATUS = models.CharField(max_length=6)
    loan_type = models.CharField(max_length=13,default="Personal_loan")

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User_type(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    flag = models.IntegerField()
    specialization = models.CharField(max_length=1200, default='NULL')


class Patient(models.Model):
    first_name = models.CharField(max_length=1200)
    last_name = models.CharField(max_length=1200)
    guardian_name = models.CharField(max_length=1200)
    city = models.CharField(max_length=1200, default='NULL')
    state = models.CharField(max_length=1200, default='NULL')
    country = models.CharField(max_length=1200, default='NULL')
    country_code = models.CharField(max_length=120, default='+91')
    zip_code = models.CharField(max_length=120, default='NULL')
    phone_number = models.CharField(max_length=1200)
    date = models.CharField(max_length=120, default='NULL')
    address = models.CharField(max_length=1200)
    problem_name = models.CharField(max_length=1200)
    assigned_doctor = models.CharField(max_length=1200)
    is_seen = models.BooleanField(default=False)


class Patient_history(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='user')
    date = models.DateField()
    diagnosis = models.CharField(max_length = 12000)
    blood_pressure = models.CharField(max_length = 1200,default='NULL')
    weight = models.CharField(max_length = 1200,default='NULL')
    sugar = models.CharField(max_length = 1200,default='NULL')
    medicine = models.CharField(max_length = 1200)
    morning_intake = models.BooleanField(default=False)
    afternoon_intake = models.BooleanField(default=False)
    evening_intake = models.BooleanField(default=False)
    days = models.IntegerField()
    tests = models.CharField(max_length=1200)
    is_done = models.BooleanField(default=False)


class Helpers_nurses(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    flag = models.IntegerField()
    contact = models.CharField(max_length=12)
    allotted_doctor = models.CharField(max_length=120)


class Medicines(models.Model):
    name = models.CharField(max_length=120)
    price = models.IntegerField()

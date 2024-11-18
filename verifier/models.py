from django.db import models

# Create your models here.

class Url(models.Model):
    nombre_url = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=False)
    message = models.CharField(max_length=100, default="No message")
    input_at = models.DateTimeField(auto_now_add=True)
    
class Email(models.Model):
    email = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=False)
    message = models.CharField(max_length=100, default="No message")
    input_at = models.DateTimeField(auto_now_add=True)
    
class Phone(models.Model):
    phone = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=False)
    message = models.CharField(max_length=100, default="No message")
    input_at = models.DateTimeField(auto_now_add=True)
    
class Sms(models.Model):
    message_sms = models.CharField(max_length=300)
    is_valid = models.BooleanField(default=False)
    message = models.CharField(max_length=100, default="No message")
    input_at = models.DateTimeField(auto_now_add=True)
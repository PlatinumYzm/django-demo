from django.db import models

# Create your models here.

class OAUser(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    email = models.EmailField()
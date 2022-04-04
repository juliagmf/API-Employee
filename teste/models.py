from unicodedata import name
from unittest import signals
from django.db import models
from uuid import uuid4
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Employee(models.Model):
    id_employee = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.CharField(max_length=30)
    salary = models.CharField(max_length=9)
    birth_date = models.DateField()
    age = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        return age


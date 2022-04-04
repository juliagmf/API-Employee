from django.db import models
from django.db.models import fields
from rest_framework import serializers
from teste.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id_employee', 'name', 'email', 'department', 'salary', 'birth_date']


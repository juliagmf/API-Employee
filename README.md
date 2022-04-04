# API-Employee

### Atualizando o sistema
```
sudo apt update 

```

```
sudo apt -y upgrade
```
### Instalando o Python3
```
sudo apt install python3-pip
```
### Instalando o env e virtualenv
```
sudo apt install -y python3-venv
```
```
sudo apt install python3-virtualenv
```
### Criando o ambiente virtual
```
virtualenv env -p python3
```
### Ativando o ambiente virtual
```
. env/bin/activate
```
### Instalando o Django
```
pip install django
```
### Criando o projeto
```
django-admin startproject core .
```
### Instalando o Django Rest Framework
```
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```
### Criando uma aplicação
```
python manage.py startapp teste
```
### Dizendo ao Django para usar a aplicação 
abra o arquivo core/settings.py
```
Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', #framework
    'teste', #app
]
```
### Criando os modelos
abra o arquivo teste/models.py 
```
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


```
### Criando um banco de dados
```
python3 manage.py migrate
```

### Criando tabelas para os modelos no banco de dados
```
python3 manage.py makemigrations teste
```
#### Aplicando ao banco de dados
```
python3 manage.py migrate teste
```
### Django Admin
abra o arquivo teste/admin.py
```
from django.contrib import admin
from teste.models import Employee

class Employees(admin.ModelAdmin):
    list_display = ('id_employee', 'name', 'email', 'department', 'salary','birth_date', 'age')
    list_display_links = ('id_employee', 'name')
    search_fields = ('name',)
    list_per_page = 20

admin.site.register(Employee, Employees)

```
### Serialização
Crie um arquivo no diretório de teste denominado serializers.py (teste/serializer.py) e adicione o seguinte código.
```
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from teste.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id_employee', 'name', 'email', 'department', 'salary', 'birth_date']


```
### Views
Edite o arquivo teste/views.py e adicione o seguinte:

```
from logging import raiseExceptions
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.db.models import Avg


from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from teste.admin import Employee
from teste.models import Employee
from teste.serializer import EmployeeSerializer



class EmployeeViewSet(viewsets.ModelViewSet):
    """Exibindo"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'salary']

    permission_classes = [permissions.IsAuthenticated]



    @action(detail=False, methods=['get'])
    def salary(self, request):
        lowest = self.queryset.order_by('salary')[0]
        highest = self.queryset.order_by('-salary')[0]
        salaryE = {
            'lowest': EmployeeSerializer(lowest).data,
            'highest': EmployeeSerializer(highest).data,
            'average': Employee.objects.all().aggregate(Avg('salary'))
        }
        print(salaryE)
        return Response(salaryE)

    @action(detail=False, methods=['get'])
    def age(self, request):
        younger = self.get_youngest()
        older = self.get_oldest()
        ageE = {
            'younger': EmployeeSerializer(younger).data,
            'older': EmployeeSerializer(older).data,
            'average': self.get_age_avg(),
        }
        print(ageE)
        return Response(ageE)

    def get_youngest(self):
        objs = self.queryset.all()
        obj = self.queryset.first()
        for i in objs:
            temp = i
            for x in objs:
                if x.age < i.age:
                    temp = i
            if temp.age < obj.age:
                obj = temp
        return obj

    def get_oldest(self):
        objs = self.queryset.all()
        obj = self.queryset.first()
        for i in objs:
            temp = i
            for x in objs:
                if x.age > i.age:
                    temp = i
            if temp.age > obj.age:
                obj = temp
        return obj
    
    def get_age_avg(self):
        total = self.queryset.count()
        ages = []
        for item in self.queryset.all():
            ages.append(int(item.age))
        average = sum(ages)//total
        return average

```
### URLs
abra o arquivo core/urls.py
```
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from teste.views import EmployeeViewSet


router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet, basename='Employees')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
]

```
### Startando o servidor
```
python3 manage.py runserver
```
### ...

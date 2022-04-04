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


   

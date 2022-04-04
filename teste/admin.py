from django.contrib import admin
from teste.models import Employee

class Employees(admin.ModelAdmin):
    list_display = ('id_employee', 'name', 'email', 'department', 'salary','birth_date', 'age')
    list_display_links = ('id_employee', 'name')
    search_fields = ('name',)
    list_per_page = 20

admin.site.register(Employee, Employees)


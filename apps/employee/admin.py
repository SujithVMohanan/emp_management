from django.contrib import admin

# Register your models here.
from .models import DynamicField, Employee


@admin.register(DynamicField)
class DynamicFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'field_type', 'order', 'section')
    list_editable = ('field_type', 'order', 'section')
    ordering = ('order',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):  
    list_display = ('id', 'dynamic_data')
    



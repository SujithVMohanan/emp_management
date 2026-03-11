from .models import DynamicField, Employee
from uuid import uuid4 as uuid
import json
from django.db import transaction
from django.core.exceptions import ValidationError




class EmployeeService:

    def __init__(self):
        pass
    
    def get_dynamic_fields(self):
        return DynamicField.objects.all().order_by('order')
    
    def get_employees(self):
        return Employee.objects.all().order_by('id')
    
    def get_employees_by_id(self, employee_id):
        try:
            employee= Employee.objects.get(id=employee_id)
            return employee.dynamic_data
        except Exception as e:
            raise ValidationError(str(e))

    @transaction.atomic
    def save_dynamic_field(self, request):
        try:
            data       = json.loads(request.body)
            section    = request.POST.get("section",None) or uuid().hex[:8]
            order      = 1
            dynamic_fields_object = []
            data       = data.get("fields", [])
            for data_value in data:
                for key, value in data_value.items():
                    print(f"Processing {key}: {value}")  # Debugging statement
                    if key == "label":
                        label = value
                    elif key == "type":
                        field_type = value
                    elif key == "section":
                        section = value

                dynamic_field = DynamicField(
                    label=label,
                    field_type=field_type,
                    order=order,
                    section=section
                )
                dynamic_fields_object.append(dynamic_field)
                order += 1

            if dynamic_fields_object:
                DynamicField.objects.all().delete()
                DynamicField.objects.bulk_create(dynamic_fields_object)

            return dynamic_fields_object
        
        except ValidationError as e:
            raise ValidationError(str(e))
        finally:
            del data
            del dynamic_fields_object   



    def save_employee(self, request):
        try:
            
            data = json.loads(request.body)
            if not data:
                raise ValidationError("No data provided.")
            
            fields = data.get("fields", [])
            if not fields:
                raise ValidationError("No fields provided.")
            employee = Employee.objects.create(dynamic_data=fields)
            return employee

        except Exception as e:
            raise ValidationError(str(e))
        
        
    def save_employee_id(self, request,employee_id):
        try:
            data = json.loads(request.body)

            if not data:
                raise ValidationError("No data provided.")

            fields = data.get("fields", {})
            if not fields:
                raise ValidationError("No fields provided.")

            employee = Employee.objects.get(id=employee_id)

            employee.dynamic_data = fields
            employee.save()

            return employee

        except Employee.DoesNotExist:
            raise ValidationError("Employee not found.")

        except Exception as e:
            raise ValidationError(str(e))
        

        
        
    def delete_employee_id(self,employee_id):
        try:
            Employee.objects.filter(id=employee_id).delete()

        except Employee.DoesNotExist:
            raise ValidationError("Employee not found.")

        except Exception as e:
            raise ValidationError(str(e))
        

        
    @transaction.atomic
    def save_serializers_dynamic_field(self, data):
        try:
            
            section    =  uuid().hex[:8]
            order      = 1
            dynamic_fields_object = []

            for data_value in data:
                for key, value in data_value.items():
                    if key == "label":
                        label = value
                    elif key == "field_type":
                        field_type = value
                    elif key == "section":
                        section = value

                dynamic_field = DynamicField(
                    label=label,
                    field_type=field_type,
                    order=order,
                    section=section
                )
                dynamic_fields_object.append(dynamic_field)
                order += 1

            if dynamic_fields_object:
                DynamicField.objects.all().delete()
                DynamicField.objects.bulk_create(dynamic_fields_object)

            return dynamic_fields_object
        
        except ValidationError as e:
            raise ValidationError(str(e))
        finally:
            del data
            del dynamic_fields_object   

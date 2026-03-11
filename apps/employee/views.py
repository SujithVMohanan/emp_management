import json

from django.forms import ValidationError
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import  JsonResponse
from django.contrib import messages

from apps.employee.services import EmployeeService
from apps.users.services import UserService
from apps.users.views import BaseTemplateView
from helpers.error_message import get_error_message


# Create your views here.



class EmployeeFeildsGenerateView(BaseTemplateView):
    template_name = "fields_generate.html"
    page_title    = "Fields Generate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "success"
        context["user"]    = self.request.user
        context["dynamic_fields"] = EmployeeService().get_dynamic_fields()
        return context




    def post(self, request, *args, **kwargs):
        try:

            employee_services = EmployeeService().save_dynamic_field(request)

            messages.success(
                request,
                f"Dynamic field updated successfully."
            )

            return JsonResponse({
                "status": True,
                "message": "Dynamic field updated successfully"
            })

        except Exception as e:
            print(f"Error during profile update: {e}")
            messages.error(request, f"{e}")
            return JsonResponse({
                "status": False,
                "message": f"Something went wrong. {e}"
            }, status=500)
        



class EmployeesView(LoginRequiredMixin,BaseTemplateView):
    template_name = "employee.html"
    page_title    = "Employees"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "success"
        context["user"]    = self.request.user
        context["dynamic_fields"] = EmployeeService().get_dynamic_fields()
        context["employees"] = EmployeeService().get_employees()
        return context


class EmployeeEditView(BaseTemplateView):    
    template_name = "employee.html"
    page_title    = "Edit Employee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "success"
        context["user"]    = self.request.user
        context["dynamic_fields"] = EmployeeService().get_dynamic_fields()
        return context


    def get(self, request, pk, *args, **kwargs):
        employee = EmployeeService().get_employees_by_id(pk)
        return JsonResponse({
            "status": True,
            "data": employee
        })
    

    def post(self, request, *args, **kwargs):
        try:
            print("kwargs",kwargs)
            employee = EmployeeService().save_employee_id(request,kwargs.get("pk"))

            messages.success(request, "Employee created successfully.")
            return JsonResponse({
                "status": "success",
                "message": "Employee created successfully."
            })  
        
        except ValidationError as e:
            print(f"Validation error during employee creation: {e}")
            messages.error(request, get_error_message(e))
            return JsonResponse({
                "status": False,
                "message": get_error_message(e)
            }, status=400)  

        except Exception as e:
            print(f"Error during employee creation: {e}")
            messages.error(request, f"Something went wrong. {e}")
            return JsonResponse({
                "status": False,
                "message": f"Something went wrong. {e}"
            }, status=500)
    
            




class EmployeeDeleteView(BaseTemplateView):
    template_name = "employee.html"
    page_title    = "Delete Employee"


    def post(self, request, *args, **kwargs):
        try:
            print("kwargs",kwargs)
            EmployeeService().delete_employee_id(kwargs.get("pk"))

            messages.success(request, "Employee deleted successfully.")
            return JsonResponse({
                "status": "success",
                "message": "Employee deleted successfully."
            })  
        
        except ValidationError as e:
            print(f"Validation error during employee creation: {e}")
            messages.error(request, get_error_message(e))
            return JsonResponse({
                "status": False,
                "message": get_error_message(e)
            }, status=400)  

        except Exception as e:
            print(f"Error during employee creation: {e}")
            messages.error(request, f"Something went wrong. {e}")
            return JsonResponse({
                "status": False,
                "message": f"Something went wrong. {e}"
            }, status=500)
    
            


class EmployeeCreateView(BaseTemplateView):
    template_name = "employee_create.html"
    page_title    = "Create Employee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "success"
        context["user"]    = self.request.user
        context["dynamic_fields"] = EmployeeService().get_dynamic_fields()
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            employee = EmployeeService().save_employee(request)

            messages.success(request, "Employee created successfully.")
            return JsonResponse({
                "status": "success",
                "message": "Employee created successfully."
            })  
        
        except ValidationError as e:
            print(f"Validation error during employee creation: {e}")
            messages.error(request, get_error_message(e))
            return JsonResponse({
                "status": False,
                "message": get_error_message(e)
            }, status=400)  

        except Exception as e:
            print(f"Error during employee creation: {e}")
            messages.error(request, f"Something went wrong. {e}")
            return JsonResponse({
                "status": False,
                "message": f"Something went wrong. {e}"
            }, status=500)
    
            
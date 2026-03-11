from django.forms import ValidationError
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import  JsonResponse
from django.contrib import messages

from apps.users.services import UserService
from helpers.error_message import get_error_message



# Create your views here.




class BaseTemplateView(TemplateView):
    """
    Base view used across project
    """

    page_title = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # global context (available everywhere)
        context["app_name"] = "Employee Management System"
        context["page_title"] = self.page_title

        return context
    


class HomeView(LoginRequiredMixin, BaseTemplateView):
    template_name = "dashboard.html"
    page_title    = "Dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "success"
        context["status"] = True
        context["user"] = self.request.user
        return context
    
    


class LoginView(BaseTemplateView):
    template_name = "login.html"
    page_title    = "Login"

    
    def __init__(self):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Hello from Advanced CBV"
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:  
                login(request,user)
                self.response_format['status_code'] = 100
                self.response_format['message']     = f"You are now logged in as {user.username}"
                self.response_format['status']      = True
                messages.success(request, f"You are now logged in as {user.username}")
            else:
                self.response_format['message'] = 'Invalid username or password'


        except Exception as e:
            self.response_format['message'] = 'Something went wrong, Please try again later.'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                username = request.user.username
                logout(request)
                messages.success(request, f"User {username} has successfully logged out.")
            else:
                messages.warning(request, "You are not logged in.")
            return redirect('users:auth_login')

        except Exception as e:
            messages.error(request, "Something went wrong while logging out.")
            return redirect('users:auth_login')
        

class RegisterView(BaseTemplateView):
    template_name = "register.html"
    page_title    = "Register"

    def __init__(self):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "success"
        return context
    
    def get_form_data(self, request):
        return {
            "email"        : request.POST.get("email"),
            "username"     : request.POST.get("username"),
            "password"     : request.POST.get("password"),
            "profile_image": request.POST.get("profile_image"),
        }
    

    def validate_data(self, data):
        if not all(data.values()):
            raise ValidationError("All fields are required.")
        
        UserService().already_exists(data)      
        
        
    def post(self, request, *args, **kwargs):

        try:
            data = self.get_form_data(request)
            self.validate_data(data)

            user = UserService().register_user_by_from_data(data)

            messages.success(
                request,
                f"User {user.username} registered successfully."
            )

            return JsonResponse({
                "status": True,
                "message": "User registered successfully"
            })

        except ValidationError as e:
            messages.error(request, str(get_error_message(e)))
            return JsonResponse({
                "status": False,
                "message": str(get_error_message(e))
            }, status=400)

        except Exception as e:
            print(f"Error during registration: {e}")
            messages.error(request, f"{e}")
            return JsonResponse({
                "status": False,
                "message": f"Something went wrong. {e}"
            }, status=500)
        

class ChangePasswordView(LoginRequiredMixin, BaseTemplateView):
    template_name = "change_password.html"
    page_title    = "Change Password"

    def __init__(self):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
    
    def get_form_data(self, request):
        return {
            "password"     : request.POST.get("password")
        }
    

    def validate_data(self, data):
        if not all(data.values()):
            raise ValidationError("All fields are required.")
        
    def post(self, request, *args, **kwargs):
        
        try:
            data = self.get_form_data(request)
            self.validate_data(data)

            user = UserService().change_password(request.user, data.get("password"))

            messages.success(
                request,
                f"User {user.username} changed password successfully."
            )

            return JsonResponse({
                "status": True,
                "message": "User password changed successfully"
            })

        except ValidationError as e:
            messages.error(request, str(get_error_message(e)))
            return JsonResponse({
                "status": False,
                "message": str(get_error_message(e))
            }, status=400)

        except Exception as e:
            messages.error(request, f"{e}")
            return JsonResponse({
                "status": False,
                "message": f"Something went wrong. {e}"
            }, status=500)
        

class ProfileView(LoginRequiredMixin, BaseTemplateView):
    template_name = "profile.html"
    page_title    = "Profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        try:

            data = {
                "email"        : request.POST.get("email"),
                "username"     : request.POST.get("username"),
                "profile_image": request.POST.get("profile_image"),
            }

            user = UserService().profile_update(request.user, data)

            messages.success(
                request,
                f"User {user.username} profile updated successfully."
            )

            return JsonResponse({
                "status": True,
                "message": "User profile updated successfully"
            })

        except Exception as e:
            print(f"Error during profile update: {e}")
            messages.error(request, f"{e}")
            return JsonResponse({
                "status": False,
                "message": f"Something went wrong. {e}"
            }, status=500)
    
            
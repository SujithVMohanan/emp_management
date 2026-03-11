
from django.urls import path
from .views import (
    EmployeeDeleteView,
    EmployeeFeildsGenerateView,
    EmployeesView,
    EmployeeCreateView,
    EmployeeEditView,
    )

app_name="employee"

urlpatterns = [
    path('fields-generate/', EmployeeFeildsGenerateView.as_view(), name='employee_fields_generate'),
    path('create/', EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('<int:pk>/edit/', EmployeeEditView.as_view(), name='employee_edit'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    
]
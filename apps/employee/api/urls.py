from django.urls import path

from apps.employee.api.views import (
    GetEmployeeApiView,
    CreateEmployeeApiView,
    DynamicFieldsListingApiView,
    CreateDynamicApiView,

)


urlpatterns = [
    path('list-employee/', GetEmployeeApiView().as_view(), name='list_employee'),
    path("create-update-delete-employee/",CreateEmployeeApiView.as_view(),name='create_employee'),

    path('fileds-list/',DynamicFieldsListingApiView.as_view(),name='list-fields'),
    path("create-or-update-fields",CreateDynamicApiView.as_view(),name='create-fields'),
]
import os
import sys
from rest_framework import generics, permissions, filters, status
from apps.employee.services import EmployeeService
from helpers.custom_response import ResponseInfo
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from helpers.pagination import RestPagination

from apps.employee.api.schema import (
    ListEmployeeSchema,
    DynamicListingSchemas,
)


from apps.employee.api.serializers import (
    EmployeeSerializer,
    DynamicCreateOrUodate,
)

from apps.employee.models import (
    Employee,
    DynamicField,
)







class GetEmployeeApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetEmployeeApiView, self).__init__(**kwargs)

    
    serializer_class    = ListEmployeeSchema
    permission_classes  = [permissions.IsAuthenticated]
    queryset            = Employee.objects.all().order_by('id')
    pagination_class    = RestPagination


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                description='Search by employee ID',
                type=openapi.TYPE_STRING
            ),
        ]

    )
    def get(self, request, *args, **kwargs):
        emp_id = request.GET.get('id', None)
        if emp_id is not None:
            employess = self.queryset.filter(id=emp_id)
        else:
            employess = self.queryset.all().order_by('id')

        page = self.paginate_queryset(employess)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class CreateEmployeeApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateEmployeeApiView, self).__init__(**kwargs)

    serializer_class = EmployeeSerializer
    response_schema  = ListEmployeeSchema
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Employee"])
    def post(self, request):
        try:
            emp_id = request.data.get("id")

            serializer = self.serializer_class(
                            instance=Employee.objects.filter(id=emp_id).first() if emp_id else None,
                            data=request.data
                        )

            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

                
            
            serializer.save()
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(tags=["Employee"],request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "id": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Employee ID"
            ),
        },))
    
    def delete(self, request):
        try:
            emp_id = request.data.get("id")

            if not emp_id:
                self.response_format.update({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "status": False,
                    "message": "Employee id is required"
                })
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            employee = Employee.objects.filter(id=emp_id).first()

            if not employee:
                self.response_format.update({
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "status": False,
                    "message": "Employee not found"
                })
                return Response(self.response_format, status=status.HTTP_404_NOT_FOUND)

            employee.delete()
            
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["message"] = "Employee deleted"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class DynamicFieldsListingApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DynamicFieldsListingApiView, self).__init__(**kwargs)

    
    serializer_class    = DynamicListingSchemas
    permission_classes  = [permissions.IsAuthenticated]
    queryset            = DynamicField.objects.all().order_by('id')
    pagination_class    = RestPagination


    @swagger_auto_schema(tags=["Fields"],
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                description='Search by employee ID',
                type=openapi.TYPE_STRING
            ),
        ]

    )
    def get(self, request, *args, **kwargs):
        fields_id = request.GET.get('id', None)
        if fields_id is not None:
            employess = self.queryset.filter(id=fields_id)
        else:
            employess = self.queryset.all().order_by('id')

        page = self.paginate_queryset(employess)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)






class CreateDynamicApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateDynamicApiView, self).__init__(**kwargs)

    serializer_class = DynamicCreateOrUodate
    response_schema  = DynamicListingSchemas
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Fields"])
    def post(self, request):
        try:

            serializer = self.serializer_class(many=True,data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            

            data = EmployeeService().save_serializers_dynamic_field(serializer.validated_data)
                       
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = self.response_schema(data,many=True).data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

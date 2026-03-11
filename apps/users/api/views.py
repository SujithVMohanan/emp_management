import os
import sys
from rest_framework import generics, permissions, filters, status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.employee.models import Employee
from apps.users.models import Users
from helpers.custom_response import ResponseInfo
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from helpers.pagination import RestPagination

from django.contrib import auth
from rest_framework.response import Response
from helpers.helpers import (
    get_object_or_none,
)

from apps.users.api.schema import (
    GetUsersSchema,
    LoginResponseSchema
)

from apps.users.api.serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterUserSerializer,
)


class LoginAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)

    serializer_class = LoginSerializer

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:

            serializer = self.serializer_class(data=request.data)
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            user = auth.authenticate(username=serializer.validated_data.get('username',''), password=serializer.validated_data.get('password',''))

            if not user:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = "Invalid username or password"
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            if user:
                
                serializer = LoginResponseSchema(user, context={"request": request})

                if not user.is_active:
                    data = {'user': {}, 'token': '', 'refresh': ''}
                    self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                    self.response_format["data"] = data
                    self.response_format["status"] = False
                    self.response_format["message"] = "Account is suspended"
                    return Response(self.response_format, status=status.HTTP_200_OK)
                
            
            refresh = RefreshToken.for_user(user)
            
            token = str(refresh.access_token)
            data = {'user': serializer.data, 'token':token, 'refresh': str(refresh)}
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
       
            
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LogoutAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    serializer_class = LogoutSerializer

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:

            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"message": "Refresh token required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["message"] = "Logout successful"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUsersApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetUsersApiView, self).__init__(**kwargs)

    
    serializer_class    = GetUsersSchema
    permission_classes  = [permissions.IsAuthenticated]
    queryset            = Users.objects.all().order_by('id')
    pagination_class    = RestPagination


    filter_backends     = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields       = ['id']

    @swagger_auto_schema(tags=["Users"],
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
        serializer = self.serializer_class(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)



class RegisterUserApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RegisterUserApiView, self).__init__(**kwargs)

    serializer_class = RegisterUserSerializer
    response_schema  = GetUsersSchema

    @swagger_auto_schema(tags=["Users"])
    def post(self, request):
        try:

            serializer = self.serializer_class(data=request.data)
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


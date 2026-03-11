"""
URL configuration for emp_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Employee Management API",
        default_version='v1',
        description="Advanced API with JWT, pagination, filters, and Swagger",
        contact=openapi.Contact(email="sujith.avrs@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),


    # include users app urls
    path('', include('apps.users.urls')),
    path('employee/', include('apps.employee.urls')),

    re_path(r'^api/', include([

        path('employee/', include('apps.employee.api.urls')),
        path('users/', include('apps.users.api.urls')),

        re_path(r'^docs/', include([
            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path("redoc", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
            

        ])), 
    ])),
]


# Serve static/media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



from django.contrib import admin

from apps.users.models import Users

# Register your models here.




@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'username', 'name', 'phone', 'email', 'is_staff', 'is_active','is_superuser', 'is_admin')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_admin')
    search_fields = ('username', 'name', 'phone', 'email')

from rest_framework import serializers

from apps.employee.models import (
    Employee,
    DynamicField,
)




class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(),required=False)

    class Meta:
        model = Employee
        fields = ['id','dynamic_data']

    def create(self, validated_data):

        employee = Employee()
        employee.dynamic_data = validated_data.get('dynamic_data',{})
        employee.save()

        return employee
    
    def update(self, instance, validated_data):
        instance.dynamic_data = validated_data.get('dynamic_data',{})
        instance.save()
        return instance
    


class DynamicCreateOrUodate(serializers.ModelSerializer):
    
    id = serializers.PrimaryKeyRelatedField(queryset=DynamicField.objects.all(),required=False)

    class Meta:
        model = DynamicField
        fields = ['id','label','field_type','order','section']
    
    


from rest_framework import serializers

from apps.employee.models import (
    Employee,
    DynamicField,
)


class ListEmployeeSchema(serializers.ModelSerializer):
    

    class Meta:
        model = Employee
        fields = ['id', 'dynamic_data']



    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas



class DynamicListingSchemas(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = ['id','label','field_type','order','section']
        

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas


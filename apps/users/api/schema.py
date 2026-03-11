from rest_framework import serializers

from apps.users.models import Users

class GetUsersSchema(serializers.ModelSerializer):
    

    class Meta:
        model = Users
        fields = ['id', 'username', 'phone', 'email', 'image', 'is_active', 'is_staff', 'is_superuser', 'is_admin']



    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas



class LoginResponseSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'phone', 'image']



    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
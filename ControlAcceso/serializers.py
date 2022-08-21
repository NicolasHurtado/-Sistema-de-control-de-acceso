from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .models import *

class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_staff = True
        user.set_password(password)
        user.save()
        models = [Usuario, Sucursal, Horario, Asignacion]
        for i in range(0,len(models)):
            content_type = ContentType.objects.get_for_model(models[i])
            permission = Permission.objects.filter(content_type=content_type)
            for perm in permission:
                user.user_permissions.add(perm)
                user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        password = validated_data.pop('password')
        instance.set_password(password)
        print(instance.user_permissions.all())
        instance.save()
        return instance
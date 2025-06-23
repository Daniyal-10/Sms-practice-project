from .models import *
from rest_framework import serializers
from django.db import transaction
from rest_framework.response import Response

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name','user_profile','password']

    # def create(self, validated_data):
    #     user = CustomUser.objects.create(validated_data)
    #     return user


class DirectorSerializer(serializers.ModelSerializer):
    user_id = CustomUserSerializer()

    class Meta:
        model = Director
        fields = "__all__"

    def create(self, validated_data):
        try:
            user_data = validated_data.pop('user_id')
            password = user_data.pop("password")
            user_profile = user_data.pop("user_profile",[])
            with transaction.atomic():    
                user = CustomUser.objects.create(**user_data)
                user.set_password(password)
                user.save()
                user.user_profile.set(user_profile)

                director = Director.objects.create(user_id=user,**validated_data)

                return  director

        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})     
        

# class DirectorSerializer(serializers.ModelSerializer):
#     user_id = CustomUserSerializer()
    
#     class Meta:
#         model = Director
#         fields = "__all__"

#     def create(self, validated_data):
#         user_data = validated_data.pop("user_id")
        
#         with transaction.atomic():
#             user = CustomUserSerializer().create(user_data)
#             director = Director.objects.create(**validated_data)

#         return director  
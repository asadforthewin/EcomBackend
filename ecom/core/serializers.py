from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer #to create a new user
from djoser.serializers import UserSerializer
from rest_framework import serializers


'''This Serializer is purely responsible for deserializing Data and creating a user record , sure we can give
it extra fields to save but thats not ideal
each software component should have a single responsibility '''


class UserCreateSerializer(BaseUserCreateSerializer): #Overriding the base serializer
    # birth_date = serializers.DateField() #as birthdate is not defined in the USER MODELs

    '''To save this we need to override the save method and change how this data is saved , so first we create a
user record and then a profile record but this is not the right way to implement this'''
    class Meta(BaseUserCreateSerializer.Meta): #inheriting from base serializer
        fields = ['id' , 'username', 'password','first_name', 'last_name', 'email' ] #adding all the fields


class UserAccessSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'id', 'username']

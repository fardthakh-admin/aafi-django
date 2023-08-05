from rest_framework import serializers
from api.models import Doctor


#
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = doctor
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = doctor.objects.create_user(validated_data['username'], validated_data['email'],
#                                           validated_data['password'])
#
#         return user

#
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = doctor
#         fields = ('id', 'username', 'email', 'password', 'role', 'gender', 'address', 'phone_number')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = doctor.objects.create_doctor(validated_data['username'], validated_data['email'],
#                                             validated_data['password'], validated_data['role'],
#                                             validated_data['gender'],
#                                             validated_data['phone_number'])
#
#         return user

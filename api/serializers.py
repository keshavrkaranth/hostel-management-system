from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *






class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'name']


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    is_student = serializers.SerializerMethodField(read_only=True)
    is_warden = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'name', 'token', 'is_student', 'is_warden']

    def get_is_student(self, obj):
        return obj.is_student

    def get_is_warden(self, obj):
        return obj.is_warden

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class StudentSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

    def get_account(self, obj):
        a = Account.objects.get(id=obj.user.id)
        return UserSerializer(a).data




class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('room_number', 'room_type', 'max_no_of_persons', 'current_no_of_persons', 'hostel')




class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ('name', 'gender', 'caretaker')

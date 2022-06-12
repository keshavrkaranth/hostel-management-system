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
        fields = ['username', 'email', 'name']


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    is_student = serializers.SerializerMethodField(read_only=True)
    is_warden = serializers.SerializerMethodField(read_only=True)
    hostel = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'name', 'token', 'is_student', 'is_warden','hostel']

    def get_is_student(self, obj):
        return obj.is_student

    def get_is_warden(self, obj):
        return obj.is_warden

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_hostel(self,obj):
        if obj.is_student:
            student = Student.objects.get(user=obj)
            gender = student.gender
            hostel = Hostel.objects.get(gender=gender)
            return hostel.id
        return None


class StudentSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    hostel = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Student
        fields = ['father_name', 'father_mbl_no', 'address', 'USN', 'branch', 'gender', 'room', 'user','hostel']


    def get_room(self, obj):
        if obj.room_allotted:
            room = obj.room
            return RoomsSerializer(room).data
        return None

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_hostel(self,obj):
        if obj.room_allotted:
            hostel = obj.room.hostel
            return HostelSerializer(hostel).data
        return None


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('room_number', 'room_type', 'max_no_of_persons', 'current_no_of_persons', 'hostel')


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ('name', 'gender', 'caretaker')


class LeaveSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    class Meta:
        model = Leave
        fields = ('id','student', 'start_date', 'end_date', 'reason', 'accept', 'reject')

    def get_student(self,obj):
        return obj.student.user.username


class RoomRepairSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomRepairs
        fields = '__all__'

import django_filters
from django_filters import FilterSet
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend, ChoiceFilter
from rest_framework import filters
from .permissions import IsWardenReadOnly, IsWarden, IsStudent

from . import serializers
from .models import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = serializers.RoomsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, IsWardenReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['hostel']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        room_type_map = ['S', 'D']
        input_map = ['room_number', 'room_type', 'maximum_number_of_persons', 'hostel']
        room_number = self.request.data.get('room_number')
        room_type = self.request.data.get('room_type')
        maximum_number_of_persons = self.request.data.get('maximum_number_of_persons')
        hostel = self.request.data.get('hostel')
        for i in input_map:
            if i not in self.request.data:
                return Response(f"{i} is required", status=status.HTTP_400_BAD_REQUEST)
        if not Hostel.objects.filter(id=hostel).exists():
            return Response("Invalid Hostel ID", status=status.HTTP_400_BAD_REQUEST)
        if room_type not in room_type_map:
            return Response("send correct room type(i.e 'S','D')", status=status.HTTP_400_BAD_REQUEST)
        if Room.objects.filter(room_number=room_number, hostel=hostel).exists():
            return Response("Room Number already exists", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HostelViewSet(ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = serializers.HostelSerializer
    permission_classes = [IsAuthenticated, IsWarden]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender']


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = serializers.StudentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'Branch', 'room', 'room__hostel']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addStudentRoom(request):
    user = request.user
    if user.is_warden:
        return Response("warden has no rights to assign room", status=status.HTTP_400_BAD_REQUEST)
    room_number = request.data.get('room_number')
    hostel = request.data.get('hostel')
    if not Room.objects.filter(room_number=room_number, hostel_id=hostel).exists():
        return Response("Invalid Room Number or Hostel id", status=status.HTTP_400_BAD_REQUEST)

    room = Room.objects.get(room_number=room_number, hostel_id=hostel)
    student = Student.objects.get(user_id=user.id)

    if room.current_no_of_persons == room.max_no_of_persons:
        return Response("Room is already filled", status=status.HTTP_400_BAD_REQUEST)

    if student.room_allotted:
        return Response("Room is already alloted for this student", status=status.HTTP_400_BAD_REQUEST)
    if not student.no_dues:
        return Response('Student has previous dues please contact warden or make payment',
                        status=status.HTTP_400_BAD_REQUEST)

    student.room = room
    student.room_allotted = True
    student.save()
    room.current_no_of_persons += 1
    room.vacant = False
    room.save()
    return Response("Room alloted for student", status=status.HTTP_200_OK)


@api_view(['POST'])
def registerStudent(request):
    request_map = ['name', 'email', 'password', 'phone_number']
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')

    for i in request_map:
        if i not in request.data:
            return Response(f"{i} is required", status=status.HTTP_400_BAD_REQUEST)
    if Account.objects.filter(email=email).exists():
        return Response("Email id already exists", status=status.HTTP_400_BAD_REQUEST)
    if Account.objects.filter(phone_number=phone_number).exists():
        return Response("Phone number already exists", status=status.HTTP_400_BAD_REQUEST)

    acc = Account.objects.create_user(name=name, username=email, email=email, password=password)
    acc.phone_number = phone_number
    acc.save()
    Student.objects.create(user=acc)
    serializer = serializers.UserSerializerWithToken(acc)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated, IsStudent])
def profile(request):
    user = request.user
    student = Student.objects.get(user=user)
    if request.method == 'GET':
        data = serializers.StudentSerializer(student).data
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        data = serializers.StudentSerializer(student,data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        student.has_filled = True
        student.save()
        return Response(data.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsStudent])
def updateProfile(request):
    user  = request.user
    student = Student.objects.get(user=user)
    data = serializers.StudentSerializer(student)
    data.is_valid(raise_exception=True)
    data.save()
    return Response(data.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homePage(request):
    warden = Warden.objects.get(id=1)

    return Response({'success': True, 'message': warden.user.is_warden}, status=status.HTTP_200_OK)

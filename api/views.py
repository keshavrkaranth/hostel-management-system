import django_filters
from django_filters import FilterSet
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend, ChoiceFilter
from rest_framework import filters
from .permissions import IsWardenReadOnly, IsWarden, IsStudent

from . import serializers
from .models import *
import datetime


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.filter(vacant=True).order_by('-created_at')
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

#TODO branch filter not working
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = serializers.StudentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'branch', 'room', 'room__hostel']

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return Response("Please login to continue", status=status.HTTP_400_BAD_REQUEST)
        if user.is_student:
            return Response("Student dont have this permissions", status=status.HTTP_400_BAD_REQUEST)
        print(user)
        warden = Warden.objects.get(user=user)
        students = Student.objects.filter(room__hostel=warden.hostel)
        serializer = serializers.StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def me(self, request):
        user = request.user
        if user.is_anonymous:
            return Response("Please login to continue", status=status.HTTP_400_BAD_REQUEST)
        if user.is_warden:
            return Response("Warden dont have this permissions", status=status.HTTP_400_BAD_REQUEST)
        student = Student.objects.get(user_id=user)
        data = serializers.StudentSerializer(student)
        return Response(data.data)


class LeaveViewSet(ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = serializers.LeaveSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    #TODO add hostel filter for warden
    def list(self, request, *args, **kwargs):
        if  request.user.is_warden:
            s = Leave.objects.all().order_by('-start_date')
            return Response(serializers.LeaveSerializer(s, many=True).data)
        else:
            return Response("Dont have permission", status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        input_map = ['start_date', 'end_date', 'reason']
        for i in input_map:
            if self.request.data.get('start_date') == '':
                return Response("Start date is required", status=status.HTTP_400_BAD_REQUEST)
            if self.request.data.get('end_date') == '':
                return Response("End date is required", status=status.HTTP_400_BAD_REQUEST)
            if i not in self.request.data:
                return Response(f"{i} is required", status=status.HTTP_400_BAD_REQUEST)
        start_date = datetime.datetime.fromisoformat(self.request.data.get('start_date'))
        end_date = datetime.datetime.fromisoformat(self.request.data.get('end_date'))
        reason = self.request.data.get('reason')
        if request.user.is_warden:
            return Response("Warden not allowed to add leave", status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        student = Student.objects.get(user=user)
        if not student.room_allotted:
            return Response("Select the room to continue with the leave application",status=status.HTTP_400_BAD_REQUEST)

        if not student.has_filled:
            return Response("Student need to fill all the profile details", status=status.HTTP_400_BAD_REQUEST)

        delta = end_date - start_date
        if delta.days >= 0 and (start_date.date() - datetime.date.today()).days >= 0:
            usr_contr = Leave.objects.filter(
                student=request.user.student, start_date__lte=end_date, end_date__gte=start_date
            )
            count = usr_contr.count()
            count = int(count)
            if count == 0:
                Leave.objects.create(student=student, start_date=start_date, end_date=end_date, reason=reason)
                return Response("Leave application submitted", status=status.HTTP_201_CREATED)
            else:
                return Response("Already in the  Leave  period", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Invalid Date', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def me(self, request):
        user_id = request.user
        if user_id.is_student:
            student = Leave.objects.filter(student__user_id=user_id)
            data = serializers.LeaveSerializer(student, many=True)
            return Response(data.data)
        return Response("Dont have permission", status=status.HTTP_400_BAD_REQUEST)


class RoomRepairsViewset(ModelViewSet):
    queryset = RoomRepairs.objects.all()
    serializer_class = serializers.RoomRepairSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            if student.room_allotted:
                repair = RoomRepairs.objects.filter(student=student)
                print(repair)
                serializer = serializers.RoomRepairSerializer(repair, many=True)
                return Response(serializer.data)
            return Response("Please select room before adding complaints", status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_warden:
            warden = Warden.objects.get(user=request.user)
            print(warden.hostel.id)
            repair = RoomRepairs.objects.filter(room__hostel__id=warden.hostel.id)
            print(repair)
            serializer = serializers.RoomRepairSerializer(repair, many=True)
            return Response(serializer.data)


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
    #TODO chane for 2 no of persons
    student.room = room
    student.room_allotted = True
    student.save()
    room.current_no_of_persons += 1
    room.vacant = False
    room.save()
    return Response("Room alloted for student", status=status.HTTP_200_OK)


@api_view(['POST'])
def registerStudent(request):
    request_map = ['name', 'email', 'password', 'phone']
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    phone = request.data.get('phone')

    for i in request_map:
        if i not in request.data:
            return Response(f"{i} is required", status=status.HTTP_400_BAD_REQUEST)
    if Account.objects.filter(email=email).exists():
        return Response("Email id already exists", status=status.HTTP_400_BAD_REQUEST)
    if Account.objects.filter(phone_number=phone).exists():
        return Response("Phone number already exists", status=status.HTTP_400_BAD_REQUEST)

    acc = Account.objects.create_user(name=name, username=email, email=email, password=password)
    acc.phone_number = phone
    acc.save()
    Student.objects.create(user=acc)
    serializer = serializers.UserSerializerWithToken(acc)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



#TODO give this permission to warden
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated, IsStudent])
def profile(request):
    user = request.user
    student = Student.objects.get(user=user)
    if request.method == 'GET':
        data = serializers.StudentSerializer(student).data
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        data = serializers.StudentSerializer(student, data=request.data, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        student.has_filled = True
        student.save()
        return Response(data.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsStudent])
def updateProfile(request):
    user = request.user
    student = Student.objects.get(user=user)
    data = serializers.StudentSerializer(student)
    data.is_valid(raise_exception=True)
    data.save()
    return Response(data.data, status=status.HTTP_200_OK)



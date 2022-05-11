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
from .permissions import IsWardenReadOnly, IsWarden

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
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'Branch', 'room', 'room__hostel']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homePage(request):
    warden = Warden.objects.get(id=1)

    return Response({'success': True, 'message': warden.user.is_warden}, status=status.HTTP_200_OK)

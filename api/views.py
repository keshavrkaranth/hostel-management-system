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

from . import serializers
from .models import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return True


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = serializers.RoomsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [MyPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['vacant', 'hostel__name', 'room_type']
    ordering_fields = ['created_at']




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homePage(request):
    warden = Warden.objects.get(id=1)

    return Response({'success': True, 'message': warden.user.is_warden}, status=status.HTTP_200_OK)

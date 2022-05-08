from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from . import serializers
from .models import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = serializers.RoomsSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['vacant','hostel']
    ordering_fields = ['created_at']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homePage(request):
    warden = Warden.objects.get(id=1)

    return Response({'success': True, 'message': warden.user.is_warden}, status=status.HTTP_200_OK)

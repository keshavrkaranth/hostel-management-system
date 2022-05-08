from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register('rooms',RoomViewSet,'rooms')


urlpatterns = router.urls + [
    path('', homePage),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

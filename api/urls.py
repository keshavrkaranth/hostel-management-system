from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register('rooms', RoomViewSet, 'rooms')
router.register('hostels', HostelViewSet, 'hostel')
router.register('students', StudentViewSet, 'students')
router.register('leaves',LeaveViewSet,'leave')

urlpatterns = router.urls + [
    path('', homePage),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('registerstudent/', registerStudent),
    path('profile/', profile),
    path('updateprofile/', updateProfile),
    path('assignstudentroom/', addStudentRoom),
]

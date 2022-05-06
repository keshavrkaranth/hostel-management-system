from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Account


@api_view(['GET'])
def homePage(request):
    return Response({'success': True, 'message': 'Working'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def createStudent(request):
    name = "Keshav R Karanth"
    email = 'Keshavarkarantha@gmail.com'
    username = '4CB18CS033'
    password = '$haShank09'

    data = Account.objects.create_user(name=name,email=email,username=username,password=password)

    return Response({'username':data.username,'permission':data.is_student},status=status.HTTP_200_OK)




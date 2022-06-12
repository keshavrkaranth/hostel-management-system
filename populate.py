import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostelmanagement.settings')

import django

django.setup()

from api.models import *
import uuid



id = 1
data = RoomRepairs.objects.filter(room__hostel_id__in=[id])
print(data)


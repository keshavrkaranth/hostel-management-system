import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostelmanagement.settings')

import django

django.setup()

from api.models import *
import uuid


data = Student.objects.all()


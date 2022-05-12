import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostelmanagement.settings')

import django

django.setup()

from api.models import Room, Hostel
import uuid



for i in Room.objects.all():
    i.delete()

#
for i in range(30):
    room_type = ['Single Occupancy', 'Double Occupancy']
    if i % 2 == 0:
        id = 0
        max_n = 1
    else:
        id = 1
        max_n = 2
    r = Room.objects.create(room_number=uuid.uuid4().hex[:6],room_type=room_type[id],max_no_of_persons=max_n,vacant=True,hostel_id=1)
    print(r)
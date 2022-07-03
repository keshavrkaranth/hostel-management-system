import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostelmanagement.settings')

import django

django.setup()

from api.helpers import sendMail

emai="keshavarkarantha@gmail.com"
sendMail(emai=emai,recipient=emai,name="Keshav",password="$haShank09")

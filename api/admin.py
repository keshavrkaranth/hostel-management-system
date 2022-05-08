from django.contrib import admin
from .models import Account,Room,Hostel,Warden,Leave
# Register your models here.

admin.site.register(Account)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Warden)
admin.site.register(Leave)

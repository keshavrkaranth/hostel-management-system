from django.contrib import admin
from .models import Account, Room, Hostel, Warden, Leave
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('name', 'username', 'email')
    exclude = ['date_joined','last_login','last_name']


admin.site.register(Account, AccountAdmin)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Warden)
admin.site.register(Leave)

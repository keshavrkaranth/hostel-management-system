from django.contrib import admin
from .models import Account, Room, Hostel, Warden, Leave, Student,RoomRepairs
from django.contrib.auth.admin import UserAdmin


# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'username',
                    'last_login', 'date_joined', 'is_admin')
    list_display_links = ('email', 'name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ['-date_joined']

    filter_horizontal = ()
    filter_vertical = ()
    fieldsets = ()


admin.site.register(Student)
admin.site.register(Account, AccountAdmin)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Warden)
admin.site.register(Leave)
admin.site.register(RoomRepairs)

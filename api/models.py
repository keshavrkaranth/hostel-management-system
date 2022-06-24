from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, name, username, email, password=None):
        if not email:
            raise ValidationError('User must have email address')
        if not username:
            raise ValidationError('User must have username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
        )
        user.set_password(password)
        user.is_active = True
        user.is_student = True
        user.save()
        return user

    def create_warden(self, name, email, username, password=None):
        if not email:
            raise ValidationError('User must have email address')
        if not username:
            raise ValidationError('User must have username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
        )
        user.set_password(password)
        user.is_warden = True
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, name, username, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save()
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_warden = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Student(models.Model):
    BRANCHES = [('N', 'None'), ('CS', 'Computer Science'), ('IS', 'Information Science'),
                ('EC', 'Electronics And Communication'),
                ('EEE', 'Electrical And Electronics'), ('ME', 'Mechanical')]
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    address = models.TextField(null=True)
    father_name = models.CharField(max_length=200, null=True)
    father_mbl_no = models.BigIntegerField(default=None, null=True)
    USN = models.CharField(max_length=10, unique=True, null=True)
    branch = models.CharField(max_length=4, choices=BRANCHES, default='N')
    dob = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True)
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default='N', null=True)
    room = models.ForeignKey(
        'Room',
        blank=True,
        on_delete=models.SET_NULL,
        null=True)
    room_allotted = models.BooleanField(default=False)
    no_dues = models.BooleanField(default=True)
    has_filled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

    def delete(self, *args, **kwargs):
        room_del = Room.objects.filter(student__room=self.room)
        for s in room_del:
            s.vacant = True
            s.save()
        super(Student, self).delete(*args, **kwargs)


class Room(models.Model):
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy')]
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(
        choices=room_choice, max_length=1, default=None)
    max_no_of_persons = models.PositiveIntegerField(default=2)
    current_no_of_persons = models.PositiveIntegerField(default=0, blank=True, null=True)
    vacant = models.BooleanField(default=True)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.room_number, self.hostel)

    def delete(self, *args, **kwargs):
        stud = Student.objects.filter(room=self)
        for s in stud:
            s.room_allotted = False
            s.save()
        super(Room, self).delete(*args, **kwargs)


class RoomRepairs(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    complaint = models.TextField()
    status = models.TextField(null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.user.username


class Hostel(models.Model):
    name = models.CharField(max_length=50)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    caretaker = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Warden(models.Model):
    user = models.OneToOneField(
        Account,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    hostel = models.ForeignKey('Hostel', default=None, null=True,
                               on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user.is_warden is False:
            self.user.is_warden = True
            self.user.save()
        super(Warden, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.is_warden = False
        self.user.save()

        super(Warden, self).delete(*args, **kwargs)


class Leave(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100, blank=False)
    accept = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    confirm_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.user.username} '


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}->{self.stock}"


class MedicineRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    remarks = models.TextField(blank=True,null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.name} -> {self.medicine.name}"

# Generated by Django 4.0.4 on 2022-05-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_hostel_room_warden_student_leave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('S', 'S'), ('D', 'D')], default=None, max_length=1),
        ),
    ]
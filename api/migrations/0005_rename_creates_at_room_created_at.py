# Generated by Django 4.0.4 on 2022-05-07 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_room_creates_at_alter_room_room_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='creates_at',
            new_name='created_at',
        ),
    ]

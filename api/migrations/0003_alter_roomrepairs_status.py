# Generated by Django 4.0.4 on 2022-06-09 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_room_repair_roomrepairs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomrepairs',
            name='status',
            field=models.TextField(null=True),
        ),
    ]

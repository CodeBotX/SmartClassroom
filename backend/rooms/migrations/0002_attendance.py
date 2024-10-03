# Generated by Django 5.0.4 on 2024-10-03 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
        ('adminpanel', '0001_initial'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Có mặt'), (2, 'Vắng mặt có phép'), (3, 'Vắng mặt không phép'), (4, 'Đi muộn')], default=1)),
                ('attendance_time', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='adminpanel.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='accounts.student')),
            ],
            options={
                'verbose_name': 'Điểm danh',
                'verbose_name_plural': 'Danh sách điểm danh',
                'db_table': 'attendance',
            },
        ),
    ]

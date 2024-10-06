# Generated by Django 5.0.4 on 2024-10-06 00:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('user_id', models.CharField(editable=False, max_length=8, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('is_parent', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='admin', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('full_name', models.CharField(max_length=255)),
                ('sex', models.CharField(blank=True, max_length=32, null=True)),
                ('day_of_birth', models.DateField(blank=True, null=True)),
                ('nation', models.CharField(blank=True, max_length=32, null=True)),
                ('active_status', models.CharField(blank=True, max_length=355, null=True)),
                ('contract_types', models.CharField(blank=True, max_length=255, null=True)),
                ('expertise_levels', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
                'db_table': 'Admin',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='parent', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('full_name', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Parent',
                'verbose_name_plural': 'Parents',
                'db_table': 'Parent',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='teacher', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('full_name', models.CharField(max_length=255)),
                ('sex', models.CharField(blank=True, max_length=32, null=True)),
                ('day_of_birth', models.DateField(blank=True, null=True)),
                ('nation', models.CharField(blank=True, max_length=32, null=True)),
                ('active_status', models.CharField(blank=True, max_length=355, null=True)),
                ('contract_types', models.CharField(blank=True, max_length=255, null=True)),
                ('expertise_levels', models.CharField(blank=True, max_length=255, null=True)),
                ('subjects', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'db_table': 'Teacher',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='student', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('full_name', models.CharField(max_length=255)),
                ('sex', models.CharField(blank=True, max_length=32, null=True)),
                ('day_of_birth', models.DateField(blank=True, null=True)),
                ('nation', models.CharField(blank=True, max_length=32, null=True)),
                ('active_status', models.CharField(blank=True, max_length=355, null=True)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='accounts.parent')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'db_table': 'Student',
            },
        ),
    ]

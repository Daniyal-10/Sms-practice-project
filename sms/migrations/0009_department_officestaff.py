# Generated by Django 5.1.2 on 2025-06-23 10:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0008_director'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OfficeStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone_no', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=10)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department', to='sms.department')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='office_staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

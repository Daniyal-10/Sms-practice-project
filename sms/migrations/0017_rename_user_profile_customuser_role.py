# Generated by Django 5.1.2 on 2025-06-24 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0016_classperiod'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='user_profile',
            new_name='role',
        ),
    ]

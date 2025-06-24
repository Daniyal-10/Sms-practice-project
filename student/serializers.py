from rest_framework import serializers
from .models import Student
from sms.models import CustomUser
from sms.models import Role
from django.db import IntegrityError
from django.core.exceptions import MultipleObjectsReturned
from sms.models import *

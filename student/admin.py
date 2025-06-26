from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Student)
admin.site.register(Guardian)
admin.site.register(StudentGuardian)
admin.site.register(GuardianType)
admin.site.register(StudentYearLevel)
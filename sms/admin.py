from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Period)
admin.site.register(YearLevel)
admin.site.register(Address)
admin.site.register(BankingDetails)
admin.site.register(Admission)
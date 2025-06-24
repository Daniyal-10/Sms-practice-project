from sms.views import * 
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'role', RoleViewSet)
router.register(r'director', DirectorViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'officestaff',OfficeStaffViewSet)



urlpatterns = [
    path('',include(router.urls)),

]
from sms.views import * 
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'role', RoleViewSet)
router.register(r'director', DirectorViewSet)



urlpatterns = [
    path('',include(router.urls)),

]
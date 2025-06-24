from teacher.views import * 
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'teacher', TeacherViewSet)

urlpatterns = [
    path('',include(router.urls)),

]
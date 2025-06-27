from sms.views import * 
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'role', RoleViewSet)
router.register(r'director', DirectorViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'officestaff',OfficeStaffViewSet)
router.register(r'country',CountryViewSet)
router.register(r'state',StateViewSet)
router.register(r'city',CityViewSet)
router.register(r'schoolyear',SchoolYearViewSet)
router.register(r'term',TermViewSet)
router.register(r'period',PeriodViewSet)
router.register(r'subject',SubjectViewSet)
router.register(r'classroomtype',ClassRoomTypeViewSet)
router.register(r'classroom',ClassRoomViewSet)
router.register(r'classperiod',ClassPeriodViewSet)
router.register(r'yearlevel',YearLevelViewSet)
router.register(r'admission',AdmissionViewSet, basename="admisson")
router.register(r'admissionupdate',AdmissionUpdateViewSet, basename="admissonupdate")



urlpatterns = [
    path('',include(router.urls)),

]
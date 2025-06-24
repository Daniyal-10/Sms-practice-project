from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extrafields):
        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        return self.create_user(email, password, **extra_fields)
    

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    # last_login = models.DateField(auto_now=True, null=True)
    first_name = models.CharField(max_length=25, null=True)
    middle_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    username = None           # removing user field
    email = models.EmailField(_("email address"), unique=True)  #setting it as username 
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # user_profile = models.FileField()


    role = models.ManyToManyField(Role,db_table='user_role', related_name='role')  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email 
    

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    phone_no = models.CharField(max_length=20)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='director')

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.department_name
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        db_table = "Department"

class OfficeStaff(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='office_staff')
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
    phone_no = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    date_joined = models.DateTimeField(auto_now=True)


class Country(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "Country"
                                

class State(models.Model):
    name = models.CharField(max_length=120)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        db_table = "State"

class City(models.Model):
    name = models.CharField(max_length=120)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        db_table = "City"


class Address(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    house_no = models.IntegerField(null=True, blank=True)
    habitation = models.CharField(max_length=100,null=True,blank=True)
    ward_no = models.IntegerField(null=True,blank=True)
    zone_no = models.IntegerField(null=True,blank=True)
    block = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    division = models.CharField(max_length=100,null=True,blank=True)
    area_code = models.IntegerField(null=True,blank=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address_line = models.CharField(max_length=250, null=True,blank=True)

    def __str__(self):
        return f"{self.user} - {self.address_line}"
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "Address"


class SchoolYear(models.Model):
    year_name = models.CharField(max_length=120)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    def __str__(self):
        return self.year_name
    
    class Meta:
        verbose_name = "School Year"
        verbose_name_plural = "School Years"
        db_table = "SchoolYear"

class Term(models.Model):
    year = models.ForeignKey(SchoolYear, on_delete=models.DO_NOTHING)
    term_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.year} - Term {self.term_number}"
    
    class Meta:
        verbose_name = "Term"
        verbose_name_plural = "Terms"
        db_table = "Term"

class Period(models.Model):
    year = models.ForeignKey(SchoolYear, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=250)
    start_period_time = models.TimeField()        
    end_period_time = models.TimeField()        

    def __str__(self):
        return f"{self.start_period_time} - {self.end_period_time} - {self.name}"
    
    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        db_table = "Period"

class Subject(models.Model):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    subject_name = models.CharField(max_length=250, null=False)

    def __str__(self):
        return f"{self.department} - {self.subject_name}"   
        
    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        db_table = "Subject"     

class ClassRoomType(models.Model):
    name = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Class Room Type"
        verbose_name_plural = "Class Room Types"
        db_table = "ClassRoomType"
        

class ClassRoom(models.Model):
    room_type = models.ForeignKey(ClassRoomType, on_delete=models.DO_NOTHING)
    room_name = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.room_type} - {self.room_name}"
    
    class Meta:
        verbose_name = "Class Room"
        verbose_name_plural = "Class Rooms"
        db_table = "ClassRoom"


class ClassPeriod(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey("teacher.Teacher", on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING)
    start_time = models.ForeignKey(
        Period, on_delete=models.DO_NOTHING, related_name="start_time"
    )  
    end_time = models.ForeignKey(
        Period, on_delete=models.DO_NOTHING, related_name="end_time"
    )
    classroom = models.ForeignKey(ClassRoom, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ClassPeriod"
        verbose_name_plural = "ClassPeriods"
        db_table = "ClassPeriod"

class BankingDetails(models.Model):
    account_no = models.BigIntegerField()
    ifsc_code = models.CharField(max_length=225)
    holder_name = models.CharField(max_length=255)
    user = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"{self.holder_name} ({self.account_no})"
    
    class Meta:
        verbose_name = "Banking Detail"
        verbose_name_plural = "Banking Details"
        db_table = "BankingDetail"

class YearLevel(models.Model):
    level_name = models.CharField(max_length=250)
    level_order = models.IntegerField()

    def __str__(self):
        return f"{self.level_name}"

    class Meta:
        verbose_name = "Year Level"
        verbose_name_plural = "Year Levels"
        db_table = "YearLevel"        
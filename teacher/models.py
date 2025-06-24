from django.db import models
from sms.models import CustomUser
# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    phone_no = models.CharField(max_length=100,null=True,blank=True)
    gender = models.CharField(max_length=50,null=True,blank=True)
    adhaar_no = models.BigIntegerField(null=True,blank=True)
    pan_no = models.BigIntegerField(null=True,blank=True)
    qualification = models.CharField(max_length=250,null=True,blank=True)

    year_levels = models.ManyToManyField('sms.YearLevel', through='TeacherYearLevel')
    
    
    
    def __str__(self):
        return f'{self.user.first_name}  {self.user.last_name}'
    

class TeacherYearLevel(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    year_level = models.ForeignKey('sms.YearLevel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'year_level')

    def __str__(self):
        return f"{self.teacher} - {self.year_level}" 

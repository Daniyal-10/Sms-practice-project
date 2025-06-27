from .models import *
from rest_framework import serializers
from django.db import transaction
from rest_framework.response import Response
from student.models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name','role','password']

class AdmissionCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name']        
    

class DirectorSerializer(serializers.ModelSerializer):
    user_id = CustomUserSerializer()

    class Meta:
        model = Director
        fields = "__all__"

    def create(self, validated_data):
        try:
            user_data = validated_data.pop('user_id')
            password = user_data.pop("password")
            role = user_data.pop("role",[])
            with transaction.atomic():    
                user = CustomUser.objects.create(**user_data)
                user.set_password(password)
                user.save()
                user.role.set(role)

                director = Director.objects.create(user_id=user,**validated_data)

                return  director

        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})     
        

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
         
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
        
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = "__all__"

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class ClassRoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomType
        fields = "__all__"
        
class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = "__all__"

class ClassPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassPeriod
        fields = "__all__"

class YearLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearLevel
        fields = "__all__"
        
class OfficeStaffSerializer(serializers.ModelSerializer):
    user_id = CustomUserSerializer()
    # department_id = DepartmentSerializer()
    class Meta:
        model = OfficeStaff
        fields = "__all__"
    def create(self, validated_data):
            try:
                user_data = validated_data.pop('user_id')
                password = user_data.pop("password")
                role = user_data.pop("role",[])
                with transaction.atomic():
                    user = CustomUser.objects.create(**user_data)
                    user.set_password(password)
                    user.save()
                    user.role.set(role)

                    officestaff = OfficeStaff.objects.create(user_id=user, **validated_data)
                    return officestaff
            except Exception as e:
                raise serializers.ValidationError({"error": str(e)})  

class AdmissonStudentSerializer(serializers.ModelSerializer):
    user = AdmissionCustomUserSerializer()
    class Meta:
        model = Student
        # fields = "__all__"
        exclude = ["classes"]

class AdmissionGuardianSerializer(serializers.ModelSerializer):
    user = AdmissionCustomUserSerializer()
    class Meta:
        model = Guardian
        fields = "__all__"

class AdmissionAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user"]

class AdmissionBankingSerailizer(serializers.ModelSerializer):
    class Meta:
        model = BankingDetails
        exclude = ["user"]


# Admission Serializer (CRUD in serializer)
class AdmissionSerializer(serializers.ModelSerializer):
    student = AdmissonStudentSerializer()
    guardian = AdmissionGuardianSerializer()
    guardian_type = serializers.CharField(write_only=True)
    # address= serializers.CharField()
    address = AdmissionAddressSerializer(write_only=True)
    banking_details = AdmissionBankingSerailizer(write_only=True)
    class Meta:
        model = Admission
        fields = "__all__"

    def create(self, validated_data):
        try:
            #Poping for user (Student)
            student_data = validated_data.pop('student')
            user_data_s = student_data.pop('user')
            password_s = user_data_s.pop('password')

            #Poping for user (Guardian)
            guardian_data = validated_data.pop('guardian')
            user_data_g = guardian_data.pop('user')
            password_g = user_data_g.pop('password')
            
            #Poping Guardian Type
            guardian_type = validated_data.pop('guardian_type')

            #Poping Address data
            address_data = validated_data.pop('address')

            #Poping Banking details
            banking_details_data = validated_data.pop('banking_details')
            
            #Popoing year level and school year
            year_level = validated_data.pop('year_level')
            school_year = validated_data.pop('school_year')
 
            with transaction.atomic():
                #Creating user setting password and role then save
                user_s = CustomUser.objects.create(**user_data_s)
                user_s.set_password(password_s)
                s = Role.objects.get(name__iexact ="Student")
                user_s.role.set([s]) 
                user_s.save()
                print(user_s)

                #Now creating student with the user
                student = Student.objects.create(user = user_s, **student_data)
                
                #Now creating Guardian with the student
                user_g= CustomUser.objects.create(**user_data_g)
                user_g.set_password(password_g)
                g = Role.objects.get(name__iexact ="Guardian")
                user_g.role.set([g])
                user_g.save()          #corrected () was missing

                #Creating Guardian
                guardian = Guardian.objects.create(user = user_g,  
                                                   **guardian_data)

                #Now assigning guardian in the admission
                #Creating guardian type
                guardian_type = GuardianType.objects.create(name = guardian_type)

                #Creating studentGuardian 
                StudentGuardian.objects.create(student = student,
                                                guardian = guardian,
                                                guardian_type = guardian_type)
                
                #Creating StudentYear Level by assinging the year and the level
                StudentYearLevel.objects.create(student = student, 
                                                level = year_level, 
                                                year = school_year)
                validated_data["year_level"]  = year_level
                validated_data["school_year"] = school_year

                #Creating Address 
                address = Address.objects.create(user = user_s, 
                                                 **address_data)

                #Adding Banking details
                banking_details = BankingDetails.objects.create(user = user_s, 
                                                                **banking_details_data)

                #Now Creating Admission
                admission = Admission.objects.create(student = student,
                                                     guardian = guardian, 
                                                    #  guardian_type = guardian_type,
                                                    #  address = address,
                                                    #  banking_details = banking_details,
                                                     **validated_data)
                
                return admission
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        return 
    

class AdmissionUpdateSerializer(serializers.ModelSerializer):
    student = AdmissonStudentSerializer(required=False)
    guardian = AdmissionGuardianSerializer(required=False)

    class Meta:
        model = Admission
        fields = '__all__'
    
    def update(self, instance, validated_data):
        #Poping for the student and the student user
        student_data = validated_data.pop("student", None)
        # Poping for the guardian and the guardian user

        # initialise to avoid UnboundLocalError
        student_user  = None
        guardian_user = None

        guardian_data = validated_data.pop("guardian", None)
        if student_data:
            student_user = student_data.pop("user", None)
            ser = AdmissonStudentSerializer(instance.student, data=student_data, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()

        if student_user:
            ser = AdmissionCustomUserSerializer(instance.student.user, data=student_user, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()

        if guardian_data:
            guardian_user = guardian_data.pop("user", None)
            ser = AdmissionGuardianSerializer(instance.guardian, data=guardian_data, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()

        if guardian_user:
            ser = AdmissionCustomUserSerializer(instance.guardian.user, data=guardian_user, partial=True)   
            ser.is_valid(raise_exception=True)
            ser.save()

        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)

        instance.save()
        return instance    
        

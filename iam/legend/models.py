from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from multiselectfield import MultiSelectField
from django.db import models
# from datetime import timedelta, date
from django.utils import timezone
# from datetime import datetime
# from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import DateTimeField
disease_CHOICES=(
    ('none', _('none')),
    ('Hypertension', _('Hypertension')),
    ('Diabetes', _('Diabetes')),
    ('asthma', _('asthma')),
    ('Kidney Disease', _('Kidney Disease')),
    ('Renal stones', _('Renal stones')),
    ('Anemia', _('Anemia')),
    ('Osteoarthritis', _('Osteoarthritis')),
    ('Rheumatoid arthritis', _('Rheumatoid arthritis')),
)
marrital_choice=(
    ('Married', _('Married')),
    ('Single', _('Single')),
    ('Divorced', _('Divorced'))
)

sex_choice = (
    ('Male', _('Male')),
    ('Female', _('Female'))
)
smoking_choice = (
    ('not smoker', _('not smoker')),
    ('Past smoker', _('Past smoker')),
    ('Active smoker', _('Active smoker')),
)
specialities = (
    ('Plastic-surgery', _('Plastic-surgery')),
    ('Internal-Medicine',_('Internal-Medicine')),
    ('General-Surgery',_('General-Surgery')),
    ('Pediatric',_('Pediatric')),
    ('Ob/Gyn', _('Ob/Gyn')),
    ('ENT', _('ENT')),
    ('Orthopedic', _('Orthopedic')),
    ('Vascular-Surgery', _('Vascular-Surgery')),
    ('Dermatology', _('Dermatology')),
    ('Ophthalmology', _('Ophthalmology')),
    ('Neurosurgery', _('Neurosurgery')),
    ('Hematology', _('Hematology')),
    ('Oncology', _('Oncology')),
    ('Radiology', _('Radiology')),
    ('Family-medicine', _('Family-medicine')),
    ('Anasthetist', _('Anasthetist')),
    ('Dentist', _('Dentist')),
    ('Maxillofacial', _('Maxillofacial')),
    ('Other', _('Other')),
    )

blood_choice = (
    ('O+', _('O+')),
    ('O-',_('O-')),
    ('AB+',_('AB+')),
    ('AB-',_('AB-')),
    ('A+',_('A+')),
    ('A-',_('A-')),
    ('B+', _('B+')),
    ('B-', _('B-')),
    ('Other', _('Other')),
    ('unknown', _('unknown')),
    )
class User (AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)



class Doctor (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(verbose_name=_('Name'),max_length=100)
    arabic_name = models.CharField(verbose_name=_('Name in a arabic'),max_length=100,default='إسم')
    speciality = models.CharField(verbose_name=_('Speciality'),max_length=200,choices=specialities, default='Plastic-surgery')
    Gender = models.CharField(max_length=50, choices=sex_choice, default='Male')
    Date_of_birth = models.DateField (default = '1990-4-20')
    adress = models.CharField(max_length=200 , default='Baghdad')
    phone_number = models.CharField(max_length=14,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    Degree = models.CharField(max_length=200, blank=True)
    Other_notes_about_your_self =models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('legend:doctor_detail', kwargs={'pk':self.pk ,'slug':self.slug , 'id':self.id})

    def __str__(self):
        return self.name




class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    doctor = models.ManyToManyField(Doctor,through='Visit',blank=True ,related_name='Patients')
    name = models.CharField(verbose_name=_('name'),max_length=100)
    Gender = models.CharField(verbose_name=_('Gender'),max_length=50, choices=sex_choice,blank=True)
    Date_of_birth = models.DateField (verbose_name=_('Birth Date'),default = _('1990-4-20'))
    adress = models.CharField(verbose_name=_('Adress'),max_length=200 , default=_('Baghdad'))
    phone_number = models.CharField(verbose_name=_('Phone number'),max_length=14,blank=True)
    Occupation = models.CharField(verbose_name=_('Occupation'),max_length=14,blank=True)
    marrital_status = models.CharField(verbose_name=_('Marital state'),max_length=50, choices=marrital_choice,blank=True)
    allergies = models.CharField(verbose_name=_('Allergies'),max_length=200, default=_('none'))
    chronic_diseases = MultiSelectField(verbose_name=_('Chronic Diseases'),choices=disease_CHOICES, blank=True)
    Other_chronic_diseases = models.CharField(verbose_name=_('Any other diseases'),max_length=200, blank=True)
    smoker = models.CharField(verbose_name=_('Smoking'),max_length=50, choices=smoking_choice, blank=True)
    Smoking_notes = models.CharField(verbose_name=_('Smoking notes'),max_length=200, blank=True)
    Next_of_kin = models.CharField(verbose_name=_('Emergency contact'),max_length=14,blank=True)
    Blood_group = models.CharField(verbose_name=_('Blood Group'),max_length=14,choices=blood_choice,blank=True)
    profile_pic = models.ImageField(verbose_name=_('Profile picture'),upload_to='profile_pics',blank=True)
    Other_notes_about_your_self =models.TextField(verbose_name=_('Notes about me'),blank=True)



    def get_absolute_url(self):
        return reverse("legend:patientdetails",kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class Visit(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient= models.ForeignKey(Patient, on_delete=models.CASCADE )
    time = DateTimeField(default=timezone.now)
    Cheif_complaint = models.CharField(max_length=200,blank=True)
    Duration=models.CharField(max_length=10,blank=True,default="1 day")
    Present_illness = models.TextField(blank=True)
    review_of_systems =models.TextField(blank=True)
    Examination =models.TextField(blank=True)
    Heart_rate=models.IntegerField(null=True,blank=True)
    Respiratory_rate=models.IntegerField(null=True,blank=True)
    Temp = models.CharField(max_length=10,blank=True)
    Visit_comments = models.TextField(max_length=200,blank=True)



    def get_absolute_url(self):
        return reverse('legend:patients_visit', kwargs={'pk':self.pk })

    def __str__(self):
        return self.doctor.name +' '+ self.patient.name



class Pressure(models.Model):
    visit = models.ForeignKey(Visit, null=True,on_delete=models.CASCADE)
    Systolic=models.IntegerField()
    Diastolic=models.IntegerField()
    time = DateTimeField(default=timezone.now)
    pressure_comments = models.TextField(max_length=200,blank=True)

    def __str__(self):
        return str(self.Systolic) +'/'+ str(self.Diastolic)

class MyPressure(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    Systolic=models.IntegerField()
    Diastolic=models.IntegerField()
    time = DateTimeField(default=timezone.now)
    pressure_comments = models.TextField(max_length=200,blank=True)

    def __str__(self):
        return str(self.Systolic) +'/'+ str(self.Diastolic)

class Investigations(models.Model):
    visit = models.ForeignKey(Visit, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='investigation')
    Value = models.CharField(max_length=200)
    time = DateTimeField(default=timezone.now)
    investigations_comments = models.TextField(max_length=200,blank=True)

    def __str__(self):
        return self.name
class MyInvestigations(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'),max_length=100,blank=True)
    Value = models.CharField(verbose_name=_('Value'),max_length=200)
    time = DateTimeField(verbose_name=_('Time'),default=timezone.now)
    investigations_comments = models.TextField(verbose_name=_('Investigation Comments'),max_length=200,blank=True)

    def __str__(self):
        return self.name
class Prescription(models.Model):
    visit = models.ForeignKey(Visit, null=True,on_delete=models.CASCADE)
    medication = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    frequency = models.CharField(max_length=200)
    directions = models.TextField(max_length=200)
    prescription_comments = models.TextField(max_length=200,blank=True)

    def __str__(self):
        return self.medication

class MyPrescription(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    medication = models.CharField(verbose_name=_('Medication'),max_length=200)
    dosage = models.CharField(verbose_name=_('Dose'),max_length=200)
    frequency = models.CharField(verbose_name=_('Frequency'),max_length=200)
    directions = models.TextField(verbose_name=_('Directions'),max_length=200)
    prescription_comments = models.TextField(verbose_name=_('Prescription Comments'),max_length=200,blank=True)

    def __str__(self):
        return self.medication
class MyNotes(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Title'),max_length=200)
    note=models.TextField(verbose_name=_('Note'),blank=True)
    time = DateTimeField(verbose_name=_('Time'),default=timezone.now)

    def __str__(self):
        return self.title

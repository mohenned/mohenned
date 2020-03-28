from django import forms
from django.forms import BaseModelFormSet
from legend.models import User ,Doctor , Patient , Visit , Pressure , Investigations ,Prescription
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
# from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse




class DateInput(forms.DateInput):
    input_type = 'date'
#####Patient forms
class PatientUserForm(forms.ModelForm):
    username = password = forms.CharField(widget=forms.TextInput(),label = _("User Name") ,help_text=_("Unique and without a space") )
    password = forms.CharField(widget=forms.PasswordInput(),label = _("Password") )
    email = forms.EmailField(widget=forms.TextInput(),label = _("Optional E-mail") ,help_text=_("You dont have to provide an e-mail,it is for password resetting."),required=False)


    class Meta():
        model = User
        fields = ('username','password','email')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        return user


class PatientUserProfileInfoForm(forms.ModelForm):

    class Meta():
        widgets = {'Date_of_birth':DateInput()}
        model = Patient
        exclude = ('user','doctor')

class PatientUpdateProfileInfoForm(forms.ModelForm):
    class Meta():
        widgets = {'Date_of_birth':DateInput()}
        model = Patient
        exclude = ('user','doctor')

class PatientUserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(),label = _("User Name") ,help_text=_("Unique and without a space") )
    email = forms.EmailField(widget=forms.TextInput(),label = _("Optional E-mail") ,help_text=_("You dont have to provide an e-mail,it is for password resetting."),required=False)


    class Meta():
        model = User
        fields = ('username','email')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        return user

#####doctor forms

class DoctorUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.TextInput(),label = "Optional E-mail" ,help_text='You dont have to provide an e-mail,it is for password resetting.',required=False)

    class Meta():
        model = User
        fields = ('username','password','email')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user


class DoctorUserProfileInfoForm(forms.ModelForm):
    class Meta():
        widgets = {'Date_of_birth':DateInput()}
        model = Doctor
        exclude = ('user',)


class DoctorUpdateProfileInfoForm(forms.ModelForm):
    class Meta():
        widgets = {'Date_of_birth':DateInput()}
        model = Doctor
        exclude = ('user',)

class DoctorUserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(),label = _("User Name") ,help_text=_("Unique and without a space") )
    email = forms.EmailField(widget=forms.TextInput(),label = _("Optional E-mail") ,help_text=_("You dont have to provide an e-mail,it is for password resetting."),required=False)


    class Meta():
        model = User
        fields = ('username','email')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user




class VisitForm(forms.ModelForm ):

    class Meta:
        model = Visit        
        exclude = ('doctor',)



class PressureForm(forms.ModelForm ):
    class Meta:
        model = Pressure
        exclude = ('visit',)
class InvestigationForm(forms.ModelForm ):
    class Meta:
        model = Investigations
        exclude = ('visit',)

class PrescriptionForm(forms.ModelForm ):
    class Meta:
        model = Prescription
        exclude = ('visit',)

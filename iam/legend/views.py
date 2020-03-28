from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .filters import DoctorFilter ,PatientFilter
from django.utils import translation
from django.views.generic import( View , TemplateView , ListView , DetailView,
                                    CreateView,UpdateView,DeleteView)
from legend import models
from legend.models import MyPressure ,MyInvestigations ,MyPrescription
from legend.forms import PatientUserForm,VisitForm,DoctorUserUpdateForm, PatientUserUpdateForm,DoctorUpdateProfileInfoForm,InvestigationForm,PrescriptionForm,PressureForm, PatientUpdateProfileInfoForm,PatientUserProfileInfoForm,PatientUserForm ,DoctorUserProfileInfoForm ,DoctorUserForm

from django.contrib.auth import authenticate, login, logout ,update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from legend.models import User , Doctor ,Patient , Visit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from .decorators import doctor_required ,patient_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm



# Create your views here.
#####common views
def home(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
            return redirect('legend:patientdetails')
        else:
            return redirect('legend:doctordetails')
    return render(request, 'legend/home.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'legend/login.html', {})
###########################################################################
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
################################
class AboutView(TemplateView):
    template_name = "legend/About.html"
#########################################3
class ThankYouView(TemplateView):
    template_name = "legend/thankyou.html"

########################################
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
#########################################
"""
All doctors views
"""

######################################
class AllDoctorsDetailView(DetailView):
    model = Doctor

    template_name = 'legend/alldoctors_details.html'
    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        return context
#####################################
def alldoctorssearch(request):
    doctors_list = Doctor.objects.all().distinct()
    doctor_filter = DoctorFilter(request.GET, queryset=doctors_list)
    return render(request, 'legend/all_doctors.html', {'filter': doctor_filter})

"""
######Patient views
"""
###patient views
def patientregister(request):
    registered = False
    if request.method == 'POST':
        user_form = PatientUserForm(data=request.POST)
        profile_form = PatientUserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
            return HttpResponseRedirect(reverse_lazy('legend:user_login'))
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = PatientUserForm()
        profile_form = PatientUserProfileInfoForm()
    return render(request,'legend/patientregistration.html',
                          {'user_form':user_form,
                          'profile_form':profile_form,
                          'registered':registered})
###########################################################
@login_required
@patient_required
def patient_detail_view(request):
    args ={'user':request.user}
    return render(request, 'legend/patientdetails.html')
############################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientDoctorsView(ListView):
    model = Patient
    template_name = 'legend/patient_doctors.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Patient.objects.get(pk=self.request.user.pk).doctor.all().distinct()
###############################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientDoctorVisitView(DetailView):
    model = Doctor

    template_name = 'legend/patientsvisitsofdoctor.html'
    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        d1=Doctor.objects.get(pk=self.kwargs['pk']).visit_set.all()
        p1=Patient.objects.get(pk=self.request.user.pk).visit_set.all()
        a=d1.intersection(p1)
        context['visit_list'] = a
        return context



############################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientVisittDetailview(DetailView):
    model = Visit
    template_name = 'legend/patientsvisitdetails.html'
    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)


        a=Visit.objects.get(pk=self.kwargs['pk']).pressure_set.all()
        context['visit_list'] = a
        b=Visit.objects.get(pk=self.kwargs['pk']).investigations_set.all()
        context['investigation_list'] = b
        c=Visit.objects.get(pk=self.kwargs['pk']).prescription_set.all()
        context['prescription_list'] = c
        return context
###############################################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientProfileUpdateView(UpdateView):
    form_class = PatientUpdateProfileInfoForm
    model = Patient
    template_name = 'legend/patient_update.html'
    success_url = reverse_lazy('legend:patientdetails')

########################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientUserUpdateView(UpdateView):
    form_class = PatientUserUpdateForm
    model = User
    template_name = 'legend/patientuser_update.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user
###################################################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientBpView(ListView):
    model = MyPressure
    template_name = 'legend/patient_pressures.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p1=Patient.objects.get(pk=self.request.user.pk).mypressure_set.all()
        context['mypressure_list'] = p1
        for visit in Patient.objects.get(pk=self.request.user.pk).visit_set.all():
            context['patientvisit_list']=visit.pressure_set.all()

        return context
##########################################
@method_decorator([login_required, patient_required], name='dispatch')
class PressureCreate(CreateView):
    model = MyPressure
    fields = ['Systolic','Diastolic','time','pressure_comments']
    template_name = 'legend/patient_pressure_create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.patient = self.request.user.patient
        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('legend:patient_BP')

#############################################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientInvestigationsView(ListView):
    model = MyInvestigations
    template_name = 'legend/patient_Investigations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p1=Patient.objects.get(pk=self.request.user.pk).myinvestigations_set.all()
        context['myinvestigations_list'] = p1
        return context

############################################################
@method_decorator([login_required, patient_required], name='dispatch')
class InvestigationsCreate(CreateView):
    model = MyInvestigations
    fields = ['name','Value','time','investigations_comments']
    template_name = 'legend/patient_investigations_create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.patient = self.request.user.patient
        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('legend:patient_Investigations')

###############################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientPrescriptionView(ListView):
    model = MyPrescription
    template_name = 'legend/patient_prescription.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p1=Patient.objects.get(pk=self.request.user.pk).myprescription_set.all()
        context['myprescription_list'] = p1

        return context
##############################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PrescriptionCreate(CreateView):
    model = MyPrescription
    fields = ['medication','dosage','frequency', 'directions','prescription_comments']
    template_name = 'legend/patient_prescription_create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.patient = self.request.user.patient
        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('legend:patient_prescription')
##############################################################
@method_decorator([login_required, patient_required], name='dispatch')
class PatientNotesView(ListView):
    model = models.MyNotes
    template_name = 'legend/patient_notes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p1=Patient.objects.get(pk=self.request.user.pk).mynotes_set.all()
        context['mynotes_list'] = p1

        return context
##########################################
@method_decorator([login_required, patient_required], name='dispatch')
class NoteCreate(CreateView):
    model = models.MyNotes
    fields = ['title','note','time']
    template_name = 'legend/patient_note_create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.patient = self.request.user.patient
        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('legend:patient_Notes')

#############################################################################
@method_decorator([login_required, patient_required], name='dispatch')
class NoteDetailview(DetailView):
    model = models.MyNotes
    template_name = 'legend/notedetails.html'

    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        return context

########
#search views
######
"""
search views
"""
####patient doctors
class SearchResultsView(ListView):
    model = Doctor
    template_name = 'legend/patient_doctors.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Patient.objects.get(pk=self.request.user.pk).doctor.filter(
            Q(name__icontains=query)|Q(arabic_name__icontains=query)
        ).distinct()
        return object_list

###########Patient visits of a doctor
class PatientsVisitsSearchView(ListView):
    model = Visit
    template_name = 'legend/patientsvisitsofdoctor.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Patient.objects.get(pk=self.request.user.pk).visit_set.filter(
            Q(time__icontains=query)
        ).distinct()
        return object_list
###########doctor patients
class DoctorPatientsSearchView(ListView):
    model = Patient
    template_name = 'legend/doctor_patients.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Doctor.objects.get(pk=self.request.user.pk).Patients.filter(
            Q(name__icontains=query)
        ).distinct()
        return object_list
#####
""""
Doctor views
"""
#####
def doctorregister(request):
    registered = False
    if request.method == 'POST':
        user_form = DoctorUserForm(data=request.POST)
        profile_form = DoctorUserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
            return HttpResponseRedirect(reverse_lazy('legend:user_login'))

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = DoctorUserForm()
        profile_form = DoctorUserProfileInfoForm()
    return render(request,'legend/doctorregistration.html',
                          {'user_form':user_form,
                          'profile_form':profile_form,
                          'registered':registered})


#######################
@login_required
@doctor_required
def doctor_detail_view(request):
    args ={'user':request.user}
    return render(request, 'legend/doctordetails.html')
##########################
@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorProfileUpdateView(UpdateView):
    form_class = DoctorUpdateProfileInfoForm
    model = Doctor
    template_name = 'legend/doctor_update.html'
    success_url = reverse_lazy('legend:doctordetails')
#########################
@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorUserUpdateView(UpdateView):
    form_class = DoctorUserUpdateForm
    model = User
    template_name = 'legend/doctoruser_update.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        '''This method will load the object
          that will be used to load the form
          that will be edited'''
        return self.request.user

#####################################################################
@login_required
@doctor_required
def doctorpatientssearch(request):
    patients_list = Doctor.objects.get(pk=request.user.pk).Patients.all().distinct()
    patient_filter = PatientFilter(request.GET, queryset=patients_list)
    return render(request, 'legend/doctor_patients.html', {'filter': patient_filter})


####################################################################
@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorPatientVisitView(DetailView):
    model = Patient
    template_name = 'legend/doctorsvisitofpatient.html'
    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        d1=Doctor.objects.get(pk=self.request.user.pk).visit_set.all()
        p1=Patient.objects.get(pk=self.kwargs['pk']).visit_set.all()
        a=d1.intersection(p1)
        context['visit_list'] = a
        return context

#####################################################################
@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorVisittDetailview(DetailView):
    model = Visit
    template_name = 'legend/doctorsvisitdetails.html'
    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)


        a=Visit.objects.get(pk=self.kwargs['pk']).pressure_set.all()
        context['visit_list'] = a
        b=Visit.objects.get(pk=self.kwargs['pk']).investigations_set.all()
        context['investigation_list'] = b
        c=Visit.objects.get(pk=self.kwargs['pk']).prescription_set.all()
        context['prescription_list'] = c
        return context

##############################################################
@method_decorator([login_required, doctor_required], name='dispatch')
class VisitCreate(CreateView):
    model = Visit
    fields = ['Cheif_complaint','Duration','Present_illness','review_of_systems','Examination','Heart_rate','Respiratory_rate','Temp','Visit_comments']
    template_name = 'legend/doctor_create_visit.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.doctor = self.request.user.doctor
        p =Patient.objects.get(user=User.objects.get(username=self.request.POST.get('username')))
        model.patient = p
        model.save()
        return HttpResponseRedirect(reverse('legend:Visit_extra',kwargs={'pk': model.pk}))

#################################################
def doctoraddpatient(request):
    registered = False
    if request.method == 'POST':
        user_form = PatientUserForm(data=request.POST)
        profile_form = PatientUserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
            return HttpResponseRedirect(reverse_lazy('legend:Visit_create'))
        else:

            print(user_form.errors,profile_form.errors)
    else:

        user_form = PatientUserForm()
        profile_form = PatientUserProfileInfoForm()

    return render(request,'legend/patientregistration.html',
                          {'user_form':user_form,
                          'profile_form':profile_form,
                          'registered':registered})
###################################
@method_decorator([login_required, doctor_required], name='dispatch')
class DuringVisitDetailview(DetailView):

    model = Visit
    template_name = 'legend/doctorextravisit.html'

    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        return context
##########################################################
@method_decorator([login_required, doctor_required], name='dispatch')
class VisitPressureCreate(CreateView):
    model = models.Pressure
    fields = ['Systolic','Diastolic','time','pressure_comments']
    template_name = 'legend/doctorvisit_pressure_create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.visit =Visit.objects.get(pk=self.kwargs['pk'])
        model.save()
        return HttpResponseRedirect(reverse('legend:Visit_extra',kwargs={'pk': model.visit.pk}))
#################################################################################
@method_decorator([login_required, doctor_required], name='dispatch')
class VisitInvestigationsCreate(CreateView):
    model = models.Investigations
    fields = ['name','Value','time','investigations_comments']
    template_name = 'legend/doctorvisit_investigations_create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.visit =Visit.objects.get(pk=self.kwargs['pk'])
        model.save()
        return HttpResponseRedirect(reverse('legend:Visit_extra',kwargs={'pk': model.visit.pk}))
#####################################################################################
@method_decorator([login_required, doctor_required], name='dispatch')
class VisitPrescriptionCreate(CreateView):
    model = models.Prescription
    fields = ['medication','dosage','frequency', 'directions','prescription_comments']
    template_name = 'legend/doctorvisit_prescription_create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.visit =Visit.objects.get(pk=self.kwargs['pk'])
        model.save()
        return HttpResponseRedirect(reverse('legend:Visit_extra',kwargs={'pk': model.visit.pk}))
#############################################################
##############################################################
@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorPatientBpView(ListView):
    model = Patient
    template_name = 'legend/doctorpatient_pressures.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p1=Patient.objects.get(pk=self.kwargs['pk']).mypressure_set.all()
        context['mypressure_list'] = p1
        context['patient_list'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context

###########################################################
class DoctorPatientInvestigationsView(ListView):
    model = Patient
    template_name = 'legend/doctorpatient_investigations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p1=Patient.objects.get(pk=self.kwargs['pk']).myinvestigations_set.all()
        context['myinvestigations_list'] = p1
        context['patient_list'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context
##################################################################
class DoctorPatientMedicationsView(ListView):
    model = Patient
    template_name = 'legend/doctorpatient_medications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p1=Patient.objects.get(pk=self.kwargs['pk']).myprescription_set.all()
        context['myprescription_list'] = p1
        context['patient_list'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context

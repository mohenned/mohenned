from django.conf.urls import url
from django.urls import path
from legend import views
from django.conf.urls.i18n import i18n_patterns
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView ,PasswordResetDoneView ,PasswordResetConfirmView,PasswordResetCompleteView
from legend.views import patientregister ,patient_detail_view ,doctor_detail_view , doctorregister,PatientProfileUpdateView

app_name = 'legend'


urlpatterns=[
    path('user_login',views.user_login,name='user_login'),
    path('about', views.AboutView.as_view(),name='about'),
    path('thankyou', views.ThankYouView.as_view(),name='thankyou'),
    path('alldoctors/<int:pk>',views.AllDoctorsDetailView.as_view(),name='alldoctors_details'),
    path('alldoctorssearch', views.alldoctorssearch, name='alldoctors_search'),

    path('patientregister',views.patientregister,name='patientregister'),
    path('patient',patient_detail_view,name='patientdetails'),
    path('patient/doctors',views.PatientDoctorsView.as_view(),name='patient_doctors'),
    path('patient/doctor/visits/<int:pk>',views.PatientDoctorVisitView.as_view(),name='patientdoctorvisits'),
    path('patient/visits/<int:pk>',views.PatientVisittDetailview.as_view(),name='patientvisitdetails'),
    path('patient/update/<int:pk>', PatientProfileUpdateView.as_view(), name='patient_update'),
    path('patient/user/update/<int:pk>', views.PatientUserUpdateView.as_view(), name='patientuser_update'),
    path('patient/visits/<int:pk>',views.PatientVisittDetailview.as_view(),name='patientvisitdetails'),
    path('patient/BP',views.PatientBpView.as_view(),name='patient_BP'),
    path('patient/BP/create/', views.PressureCreate.as_view(), name='BP_create'),
    path('patient/Investigations',views.PatientInvestigationsView.as_view(),name='patient_Investigations'),
    path('patient/Investigations/create/', views.InvestigationsCreate.as_view(), name='Investigations_create'),
    path('patient/Prescription',views.PatientPrescriptionView.as_view(),name='patient_prescription'),
    path('patient/Prescription/create/', views.PrescriptionCreate.as_view(), name='Prescription_create'),
    path('patient/doctors/search',views.SearchResultsView.as_view(),name='search_results'),
    path('patient/doctors/visits/search',views.PatientsVisitsSearchView.as_view(),name='patientsvisits_search_results'),
    path('patient/Notes',views.PatientNotesView.as_view(),name='patient_Notes'),
    path('patient/Note/create/', views.NoteCreate.as_view(), name='Note_create'),
    path('patient/Note/<int:pk>',views.NoteDetailview.as_view(),name='note_details'),

    path('doctorregister',views.doctorregister,name='doctorregister'),
    path('doctor',doctor_detail_view,name='doctordetails'),
    path('doctor/update/<int:pk>', views.DoctorProfileUpdateView.as_view(), name='doctor_update'),
    path('doctor/user/update/<int:pk>', views.DoctorUserUpdateView.as_view(), name='doctoruser_update'),
    path('doctor/patients', views.doctorpatientssearch, name='doctor_patients'),
    path('doctor/patients/search',views.DoctorPatientsSearchView.as_view(),name='doctor_patients_search'),
    path('doctor/patient/visits/<int:pk>',views.DoctorPatientVisitView.as_view(),name='doctorpatientvisits'),
    path('doctor/patientBP/<int:pk>',views.DoctorPatientBpView.as_view(),name='doctor_patientBP'),
    path('doctor/patientinvestigations/<int:pk>',views.DoctorPatientInvestigationsView.as_view(),name='doctor_patientinvestigations'),
    path('doctor/patientmedications/<int:pk>',views.DoctorPatientMedicationsView.as_view(),name='doctor_patientmedications'),
    path('doctor/visits/<int:pk>',views.DoctorVisittDetailview.as_view(),name='doctorvisitdetails'),
    path('doctor/visit/create/', views.VisitCreate.as_view(), name='Visit_create'),
    path('doctor/visit/create/addpatient',views.doctoraddpatient,name='add_patient'),
    path('doctor/visit/create/extra/<int:pk>', views.DuringVisitDetailview.as_view(), name='Visit_extra'),
    path('doctor/visit/create/extra/<int:pk>/BP/create', views.VisitPressureCreate.as_view(), name='visitBP_create'),
    path('doctor/visit/create/extra/<int:pk>/investigation/create', views.VisitInvestigationsCreate.as_view(), name='visitInv_create'),
    path('doctor/visit/create/extra/<int:pk>/prescription/create', views.VisitPrescriptionCreate.as_view(), name='visitpresc_create'),


]

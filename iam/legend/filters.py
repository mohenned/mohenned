from legend.models import Doctor , Patient
import django_filters

class DoctorFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = ['speciality', 'name', 'arabic_name', ]


class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        fields = [ 'name', 'Gender','adress','phone_number','Occupation','marrital_status','allergies','chronic_diseases','smoker','Blood_group', ]

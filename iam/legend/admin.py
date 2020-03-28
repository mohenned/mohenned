from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import User , Patient , Doctor , Visit ,Pressure,Prescription,Investigations ,MyPressure,MyPrescription,MyInvestigations


admin.site.register (User,UserAdmin)
admin.site.register (Patient)
admin.site.register (Doctor)
admin.site.register (Visit)
admin.site.register (Pressure)
admin.site.register (Prescription)
admin.site.register (Investigations)
admin.site.register (MyPressure)
admin.site.register (MyInvestigations)
admin.site.register (MyPrescription)

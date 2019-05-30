from django.contrib import admin
from .models import Responsable, Clinicien, Patient, Journal
# Register your models here.


class ResponsableAdmin(admin.ModelAdmin):
    list_display   = ('username')
    list_filter    = ('hopital')
    date_hierarchy = 'user.date_joined'
    ordering       = ('user.date_joined', )
    search_fields  = ('hopital')

class ClinicienAdmin(admin.ModelAdmin):
    list_display   = ('username')
    list_filter    = ('hopital', 'Responsable')
    date_hierarchy = 'user.date_joined'
    ordering       = ('user.date_joined', )
    search_fields  = ('hopital', 'Responsable')

admin.site.register(Responsable)#,ResponsableAdmin )
admin.site.register(Clinicien)#,ClinicienAdmin )
admin.site.register(Patient)
admin.site.register(Journal)
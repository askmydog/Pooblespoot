from django.contrib import admin
from medrec_v2.models import BaseMed, Medication, MedQualifier, MedType, MedRoute, DoseLookup, DateLookup, SigLookup, InstLookup
from medrec_v2.forms import SigForm

# Register your models here.

app_name="medrec_v2"

@admin.register(BaseMed)
class BaseMedAdmin(admin.ModelAdmin):
    ordering = ['base_med_name']
    search_fields = ['base_med_name', 'base_med_type__type_name']
    list_display = ['base_med_name']
    readonly_fields = ['base_med_regex']

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    ordering = ['med_1']
    search_fields = [
        # 'med_1',
        # 'med_2',
        # 'med_3',
        'display_name',
        # # 'med_route__route_name',
        # # 'med_type__type_name',
        'med_qualifiers__qual_name',
        # 'med_commonuses'
        ]
    list_display = ['display_name' ]
    autocomplete_fields = ['med_1', 'med_2', 'med_3', 'med_4', 'med_qualifiers', 'med_route']
    readonly_fields = [ 'med_pronun', 'med_type_str', 'regex_med_1', 'regex_med_2', 'regex_med_3','regex_med_4',]

@admin.register(MedQualifier)
class MedQualifierAdmin(admin.ModelAdmin):
    search_fields = ['qual_name']
    list_display = ['qual_name','qual_desc', 'qual_regex']
    readonly_fields = ['qual_regex']

@admin.register(MedType)
class MedTypeAdmin(admin.ModelAdmin):
    search_fields = ['type_name',]
    list_display = ['type_name', 'type_desc']

@admin.register(MedRoute)
class MedRouteAdmin(admin.ModelAdmin):
    search_fields = ['route_name',]
    list_display = ['route_name', 'route_desc', 'route_regex']
    readonly_fields = ['route_regex',]

@admin.register(DoseLookup)
class DoseLookupAdmin(admin.ModelAdmin):
    list_display = ['dose_num','dose_regex',]  

@admin.register(DateLookup)
class DateLookupAdmin(admin.ModelAdmin):
    list_display = ['date_num','date_regex',] 

@admin.register(InstLookup)
class InstLookupAdmin(admin.ModelAdmin):
    list_display = ['inst_num','inst_regex',] 

@admin.register(SigLookup)
class SigLookupAdmin(admin.ModelAdmin):
    search_fields = ['sig_name', 'sig_regex',]
    list_display = ['sig_name', 'sig_plain_text', 'sig_regex',] 
    readonly_fields = ['sig_regex']
    form = SigForm
from django.contrib import admin

# Register your models here.
from .models import Patient, Med, MedInstance, Indication, Frequency, Route

#admin.site.register(Patient)
#admin.site.register(Med)
#admin.site.register(MedInstance)
admin.site.register(Indication)
admin.site.register(Frequency)
admin.site.register(Route)

# Define the admin class
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
    fields = [('last_name', 'first_name'), 'date_of_birth']

# Register the admin class with the associated model
admin.site.register(Patient, PatientAdmin)


class MedInstanceInline(admin.TabularInline):
    model = MedInstance
# Register the Admin classes for Book using the decorator
@admin.register(Med)
class MedAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'dose', 'route', 'display_indication')
    inlines = [MedInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(MedInstance) 
class MedInstanceAdmin(admin.ModelAdmin):
    list_filter = ('patient', 'status', 'med')
    fieldsets = (
    	(None, {
        	'fields': ('patient', 'med', 'frequency', 'prescriber', 'id')
    	}),
    	('Patient Information', {
        	'fields': ('date_prescribed', 'date_filled', 'status')
    	}),
	)
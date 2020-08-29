from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from meddatabase.models import Med, Patient, MedInstance, Indication

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_meds = Med.objects.all().count()
    num_instances = MedInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_out = MedInstance.objects.filter(status__exact='o').count()
    
    # The 'all()' is implied by default.    
    num_patients = Patient.objects.count()
    
    context = {
        'num_meds': num_meds,
        'num_instances': num_instances,
        'num_instances_out': num_instances_out,
        'num_patients': num_patients,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
    
from django.views import generic

class MedListView(generic.ListView):
    model = Med
    paginate_by = 25

class MedDetailView(generic.DetailView):
    model = Med

class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient

 
class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Patient
    paginate_by = 25
    
class PrescribedMedsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = MedInstance
    template_name ='meddatabase/medinstance_list_prescribing_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return MedInstance.objects.filter(prescriber=self.request.user).filter(status__exact='o').order_by('date_prescribed')
        
import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from meddatabase.models import Med
from django.template import RequestContext
from meddatabase.forms import MedRecForm

@permission_required('meddatabase.can_reconcile_meds')
def rec_meds_corpsman(request):
    query = request.GET.get('q')
    results = None
    try:
        query
    except ValueError:
        query = None
        results = None
    if query:
        results = Med.objects.get(medication_name=query)
    context = RequestContext(request)
    return render('output_page.html', {"results": results,})
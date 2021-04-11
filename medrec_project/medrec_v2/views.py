from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from medrec_v2.scripts.medrec_v2.functions import med_match, csv_fk_field_builder, med_match_v2, extract_dose
from django.contrib import messages
from django.db.models import F, Q

from medrec_v2.models import Medication, MedQualifier, MedRoute, MedType, BaseMed
from medrec_v2.forms import MedInputForm, AddMedForm
import re, json, csv, io

class MedInputView(View):
    form_class = MedInputForm
    template_name = 'medrec_v2/med_input.html'
    med_urls = {}
    med_set = Medication.objects.all()
    # for med in Medication.objects.all():
    #     med_urls[med.pk]=med.get_absolute_url()
        # print(med.get_absolute_url())
    # print(med_urls)
    # med_urls = json.dumps(med_urls)


    def get(self, request):
        form = self.form_class()
        context = {'form':form, "med_set":self.med_set}
        return render(request, self.template_name, context)



class postMedRec(View):
    form_class = MedInputForm
    template_name = 'medrec_v2/med_input.html'
    med_match = {}
    med_set = Medication.objects.all()

    def post(self, request):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)

            if form.is_valid():
                json_dict = {}
                json_dict['line'] = []
                json_list = []
                
                input_meds = form.cleaned_data['input_meds']
                input_meds = input_meds.split('\n')
                for input_line in input_meds:
                    input_line = input_line.strip()
                    if input_line != '':
                        json_med = med_match_v2(input_line)
                        json_list.append(json_med)
                        [json_dict['line'].append(x) for x in json_list if x not in json_dict['line']]
                ser_meds = json.dumps(json_dict, default=lambda o: o.__dict__)
                return JsonResponse({'med_output':ser_meds}, status = 200)    
            else:
                return JsonResponse({"error", form.errors}, status= 200)
        return JsonResponse({"error":""}, status=400)



class AddMedView(CreateView):
    model = Medication
    form_class = AddMedForm
    template_name_suffix = '_create_form'
    # fields = ['med_1','trade_name','reg_match_1','med_match_2']

class MedicationDetail(DetailView):
    model=Medication         

class MedicationList(ListView):
    model=Medication

class MedDbUpload(View):
    template_name = 'medrec_v2/med_upload.html'
    meds = Medication.objects.all()   
    base_meds = BaseMed.objects.all()

    def get(self, request, *args, **kwargs):
        prompt = {
            'order': 'Order of the CSV should be med_name, med_regex, med_pronun, med_type, med_interactions, med_notes',
            'meds': self.meds,
            'Base Meds':self.base_meds
        }
        return render(request, self.template_name, prompt)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['file']
        db_select = request.POST.get('db_select')
        if not csv_file.name.endswith(".csv"):
            messages.error(request, 'THIS IS NOT A CSV FILE')

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        if db_select == "db_base":
            for column in csv.reader(io_string, delimiter=','):
                csv_name = column[0].title()
                csv_regex = column[1]
                csv_pronun = column[2]
                csv_type = csv_fk_field_builder(column[3].lower(), MedType, 'type_name')
                csv_interactions = csv_fk_field_builder(column[4].lower(), MedType, 'type_name')
                csv_notes = column[5]
                try:
                    csv_med = BaseMed.objects.get(
                        med_name__iexact = csv_name
                    )
                    csv_med.med_regex = csv_regex
                    csv_med.med_pronun = csv_pronun
                    if csv_type:
                        if type(csv_type) is int:
                           csv_med.med_type.add(MedType.objects.get(id=csv_type))
                        else:
                            for item in csv_type:
                                csv_med.med_type.add(MedType.objects.get(id=item))
                    if csv_interactions:
                        if type(csv_interactions) is int:
                           csv_med.med_interactions.add(MedType.objects.get(id=csv_interactions))
                        else:
                            for item in csv_interactions:
                                csv_med.med_interactions.add(MedType.objects.get(id=item))
                    csv_med.med_notes = csv_notes
                    csv_med.save()

                except BaseMed.DoesNotExist:
                    csv_med = BaseMed.objects.create(
                        med_name = csv_name,
                        med_regex = csv_regex,
                        med_pronun = csv_pronun,
                        med_notes = csv_notes
                    )
                    if csv_type:
                        if type(csv_type) is int:
                           csv_med.med_type.add(MedType.objects.get(id=csv_type))
                        else:
                            for item in csv_type:
                                csv_med.med_type.add(MedType.objects.get(id=item))
                    if csv_interactions:
                        if type(csv_interactions) is int:
                           csv_med.med_interactions.add(MedType.objects.get(id=csv_interactions))
                        else:
                            for item in csv_interactions:
                                csv_med.med_interactions.add(MedType.objects.get(id=item))
                    csv_med.save()                    
                    
            context = {'meds':self.base_meds}
            return render(request, self.template_name, context)            

        else:
            for column in csv.reader(io_string, delimiter=','):
                csv_med_1 = csv_fk_field_builder(column[0], BaseMed, 'med_name')
                csv_med_2 = csv_fk_field_builder(column[1], BaseMed, 'med_name')
                csv_med_3 = csv_fk_field_builder(column[2], BaseMed, 'med_name')
                csv_med_4 = csv_fk_field_builder(column[3], BaseMed, 'med_name')
                csv_med_tr = column[4]
                csv_qual = csv_fk_field_builder(column[5], MedQualifier, 'qual_name')
                csv_regex = column[6]
                csv_route = csv_fk_field_builder(column[7], MedRoute, 'route_name')
                csv_commonuses = column[8]
                csv_notes = column[9]

                med_lookups = Q(med_1 = BaseMed.objects.get(id=csv_med_1))
                if csv_med_2 is not None: med_lookups = med_lookups & Q(med_2 = BaseMed.objects.get(id=csv_med_2))
                else: med_lookups = med_lookups & Q(med_2__isnull = True)

                if csv_med_3 is not None: med_lookups = med_lookups & Q(med_3 = BaseMed.objects.get(id=csv_med_3))
                else: med_lookups = med_lookups & Q(med_3__isnull = True)

                if csv_med_4 is not None: med_lookups = med_lookups & Q(med_4 = BaseMed.objects.get(id=csv_med_4))
                else: med_lookups = med_lookups & Q(med_4__isnull = True)

                if csv_route is not None: med_lookups = med_lookups & Q(med_route = MedRoute.objects.get(id=csv_route))
                else: med_lookups = med_lookups & Q(med_route__isnull = True)

                if csv_med_tr != '': tr_lookups = Q(trade_name__icontains = csv_med_tr)
                else: tr_lookups = Q(trade_name__exact = "")

                if csv_qual is not None: 
                    if type(csv_qual) is int:
                        qual_lookups = Q(med_qualifiers = MedQualifier.objects.get(id=csv_qual))
                    else:
                        for i in range(len(csv_qual)):
                            if i == 0: qual_lookups = Q(med_qualifiers = MedQualifier.objects.get(id=csv_qual[i]))
                            else: qual_lookups = qual_lookups | Q(med_qualifiers = MedQualifier.objects.get(id=csv_qual[i]))
                else:
                    qual_lookups = Q(med_qualifiers__isnull = True)

                try:
                    csv_med = Medication.objects.get(med_lookups, tr_lookups, qual_lookups)

                    if csv_med.med_qualifiers is None and csv_qual is not None:
                        if type(csv_qual) is int: csv_med.med_qualifiers.add(MedQualifier.objects.get(id=csv_qual))
                        else: 
                            for item in csv_qual:
                                csv_med.med_qualifiers.add(MedQualifier.objects.get(id=item))
                    csv_med.med_regex = csv_regex
                    csv_med.med_commonuses = csv_commonuses
                    csv_med.med_notes = csv_notes
                    csv_med.save()

                except (Medication.DoesNotExist, BaseMed.DoesNotExist):
                    csv_med = Medication.objects.create(
                        med_1 = BaseMed.objects.get(id=csv_med_1)
                    )
                    if csv_med_2 is not None:
                        setattr(csv_med, 'med_2', BaseMed.objects.get(id=csv_med_2))
                    if csv_med_3 is not None:
                        setattr(csv_med, 'med_3', BaseMed.objects.get(id=csv_med_3))
                    if csv_med_4 is not None:
                        setattr(csv_med, 'med_4', BaseMed.objects.get(id=csv_med_4))
                    csv_med.trade_name =  csv_med_tr
                    csv_med.med_regex = csv_regex
                    if csv_route is not None:
                        # print(f'views.py --> med_route: {MedRoute.objects.get(id = csv_route)}')
                        # print(f'views.py --> csv_med._meta.fields {csv_med._meta.fields}')
                        setattr(csv_med, 'med_route', MedRoute.objects.get(id=csv_route))
                    csv_med.med_commonuses = csv_commonuses
                    csv_med.med_notes = csv_notes
                    if csv_qual is not None:
                        if type(csv_qual) is int: csv_med.med_qualifiers.add(MedQualifier.objects.get(id=csv_qual))
                        else: 
                            for item in csv_qual: csv_med.med_qualifiers.add(MedQualifier.objects.get(id=item))
                    csv_med.save()
                
                except MedQualifier.DoesNotExist:
                    if tr_lookups != '': csv_med = Medication.objects.get(med_lookups, tr_lookups)
                    else: csv_med = Medication.objects.get(med_lookups)

                    if csv_med.med_qualifiers is None and csv_qual is not None:
                        if type(csv_qual) is int: csv_med.med_qualifiers.add(MedQualifier.objects.get(id=csv_qual))
                        else: 
                            for item in csv_qual: csv_med.med_qualifiers.add(MedQualifier.objects.get(id=item))
                    csv_med.save()

                except Medication.MultipleObjectsReturned:
                    continue
                

            context = {'meds':Medication.objects.all()}
            return render(request, self.template_name, context)

# Create your views here.
import re, os
from medrec_v2.models import Medication, MedQualifier, MedRoute, MedType, DoseLookup, InstLookup, DateLookup, SigLookup
from inspect import currentframe, getframeinfo
# from django.db.models import F
# from django.db.models.options import Options


med_set = Medication.objects.all()
med_quals  = MedQualifier.objects.all()
med_routes = MedRoute.objects.all()
med_types = MedType.objects.all()



# MatchListClass - class of an object that can collect a list of matches and 
# match indicies and return the highest matching medication 

class MatchListClass:

    def __init__(self, line_input, error=""):
        self.line_input = line_input
        self.dose = extract_dose(line_input)
        self.sig = extract_sig(line_input)
        self._matches = set()
        self._remove_med = set()
        self._max_match = set()
        self.error = error
        
    def __repr__(self):
        return f'{self.line_input} [{self.matches}]'
        
    @property
    def matches(self):
        return self._matches

    # add new medications to the match list --> added med contains match index 
    def add_med(self, med):
        self._matches.add(med)
        
    def remove_med(self, med):
        for meds in self._matches:
            if med in meds.med_name:
                self._remove_med.update([meds])
                del meds
        self._matches.difference_update(self._remove_med)

    @property
    def _max_index(self):
        if len(self._matches)>0:
            return max([m.match_index for m in self._matches])
        else:
            return 0
    
    @property
    def max_match(self):
        self._max_match.clear()
        if len(self._matches)>0:
            _max_idx = self._max_index
            for i in self._matches:
                if i.match_index ==_max_idx:
                    self._max_match.add(Medication.objects.get(pk = i.pk))
            return list(self._max_match)
        else:
            return list()
    
    @property
    def final_match(self):
        return [self.line_input, self.max_match, self.dose, self.sig]

        
# MatchedMedClass: class of objects that can store relevant information about medications that
# match the regex string in the main med_match function
class MatchedMedClass:
    
    def __init__(self, med, match_index):
        self.med = med

        self.regex_med_1 = med.regex_med_1

        if med.med_2 is not None: 
            self.regex_med_2 = med.regex_med_2
        else: self.regex_med_2 = None

        if med.med_3 is not None: 
            self.regex_med_3 = med.regex_med_3
        else: self.regex_med_3 = None 

        if med.med_4 is not None: 
            self.regex_med_4 = med.regex_med_4
        else: self.regex_med_4 = None

        if med.med_route is not None: 
            self.regex_route = med.regex_route
        else: self.regex_route = None

        if med.med_qualifiers is not None: 
            self.regex_qual = med.regex_qual
        else: self.regex_qual = None

        self.pk = med.pk

        self.match_index=match_index
        
    def __repr__(self):
        return f'{self.med}: {self.match_index}'



def med_match(input_meds):
    i=1
    match_list = MatchListClass(input_meds)
    print('functions.py:med_match:input_meds')
    print(input_meds)
    
   
    for med_1 in med_set:
        re_mm1 = med_1.reg_match_1
        if re.search(re_mm1, input_meds, re.IGNORECASE):
            print('med_1')
            print(med_1)
            
            print('re_mm1')
            print(re_mm1)
            med=MatchedMedClass(med_1.pk, med_1.display_name, i)
            match_list.add_med(med)
            
    if len(match_list.matches) == 0:
        match_list.error = "No Matches!"
        return [match_list.line_input, match_list.error]

    else:
        for med_2 in match_list.matches:
            med2 = med_set.get(pk=med_2.med_pk)

            if med2.med_match_2 != '':
                if re.search(med2.med_match_2,input_meds,re.IGNORECASE):
                    med_2.med_index += 1
                else:
                    med_2.med_index -= 1
            
            # -----------NEED TO BE ABLE TO SEARCH FOR FOREIGN KEYS/Many-to-many------------
            if med2.med_qualifiers.all().count()>0:
                med2_qual = med2.reg_qual
                print('functions.py:med_match:med2_qual')
                print(med2_qual)
                if re.search(med2_qual, input_meds, re.IGNORECASE):
                    med_2.med_index += 1
                else:
                    med_2.med_index -= 1

            # if med2.med_route != '':
            #     if re.search(med2.med_route,input_meds,re.IGNORECASE):
            #         med_2.med_index += 1
            #     else:
            #         med_2.med_index -= 1
        print('match_list.max_match')
        print(match_list.max_match)
        return match_list.max_match






def med_match_v2(input_meds):

    match_list = MatchListClass(input_meds)

    for med in med_set:
        if med.trade_name != "":
            if re.search(med.trade_name, input_meds, re.IGNORECASE):
                med_new = MatchedMedClass(med, 1)
                match_list.add_med(med_new)

    copy_match_list = match_list.matches.copy()
    
    for med in med_set:
        
        if re.search(med.regex_med_1, input_meds, re.IGNORECASE):
            match_chk = False
            for item in copy_match_list:            
                if med.pk == item.pk:
                    match_chk = True
            if match_chk == False:           
                match_list.add_med(MatchedMedClass(med, 1))

    if len(match_list.matches) == 1:
        return match_list.final_match
    
    for match in match_list.matches:
        if match.regex_med_2 is not None: 
            if re.search(match.regex_med_2, input_meds, re.IGNORECASE):
                match.match_index += 1
            else:
                match.match_index -= 1

            if match.regex_med_3 is not None:    
                if re.search(match.regex_med_3, input_meds, re.IGNORECASE):
                    match.match_index += 1
                else:
                    match.match_index -= 1    

                if match.regex_med_4 is not None:    
                    if re.search(match.regex_med_4, input_meds, re.IGNORECASE):
                        match.match_index += 1
                    else:
                        match.match_index -= 1 

        if match.regex_route is not None:
            if re.search(match.regex_route, input_meds, re.IGNORECASE):
                match.match_index += 1
            else:
                match.match_index -= 1

        if match.regex_qual is not None:
            if re.search(match.regex_qual, input_meds, re.IGNORECASE):
                match.match_index += 1
            else:
                match.match_index -= 1
        
    return match_list.final_match






def csv_fk_field_builder(csv_input, fk_model, fk_name_field, fk_reg_field=None):
    item_list = []
    if csv_input != '':
        items = csv_input.split(', ')
        if len(items) == 1:
            if fk_model.objects.filter(**{fk_name_field+"__iexact":items[0]}):
                return fk_model.objects.get(**{fk_name_field+"__iexact":items[0]}).id
            else:
                return fk_model.objects.create(**{fk_name_field: items[0]}).id

        for item in items:
            if not fk_model.objects.filter(**{fk_name_field+'__iexact': item}):
                if fk_reg_field is None:
                    fk_model.objects.update_or_create(**{fk_name_field: item})
                else:
                    fk_model.objects.update_or_create(**{fk_name_field: item, fk_reg_field: item})
                item_list.append(fk_model.objects.get(**{fk_name_field: item}).id)
            else:
                item_list.append(fk_model.objects.get(**{fk_name_field+'__iexact': item}).id)
    #     if len(item_list) == 1: 
    #         item_str = item_list
    #     else: 
    #         item_str = ', '.join(item_list)
    else: 
        item_list = None

    return item_list

def display_name_builder(generic_name, trade_name):
    if trade_name == '': 
        display_name = generic_name.capitalize()              
    else:
        display_name = trade_name.capitalize() + ' (' + generic_name.upper() + ')'
    return display_name        
# def return_max_matches(med_list):
#     mult_match =[]
#     max_match_index = max(m['match_index'] for m in med_list)
#     for med in med_list:
#         if med['match_index'] < max_match_index:
#           med_list.remove(med)
#     if len(med_list) >1:
#         mult_match = med_list
#     #     max_med_match = MatchedMedList['meds'].filter('match_index'=max_match_index)
#     return med_list


def extract_dose(input_text):
    dose_regex = DoseLookup.objects.get(dose_num=1).dose_regex
    dose_text = re.search(dose_regex, input_text, re.IGNORECASE)
    if dose_text is not None:
        return dose_text.group()   
    else: return ''

def extract_sig(input_text):
    regex_list=[]

    for sig in SigLookup.objects.all():
        input_text = re.sub(sig.sig_regex, sig.sig_plain_text,input_text,re.I)

    inst_regex_1 = InstLookup.objects.get(inst_num=1).inst_regex
    if re.search(inst_regex_1, input_text, re.I):
        regex_list.append(re.search(inst_regex_1, input_text, re.I).group())

    inst_regex_2 = InstLookup.objects.get(inst_num=2).inst_regex
    if re.search(inst_regex_2, input_text,re.I):
        regex_list.append(re.search(inst_regex_2, input_text,re.I).group())
    
    return ''.join(regex_list)



def debug_print(text:str, arg, current_frame=currentframe()):
    frame_info = getframeinfo(current_frame)
    file_name = os.path.basename(frame_info.filename)
    print(f'{file_name} ln:{current_frame.f_back.f_lineno} >> {text}: {arg}')



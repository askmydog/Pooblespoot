from django.db import models
from django.urls import reverse
import re, os
from django.db.models import Lookup, Field, Q
from inspect import currentframe, getframeinfo




class BaseMed(models.Model):
    base_med_name = models.CharField(max_length=200, verbose_name='Base Medication Name', unique=True)
    base_med_add_terms = models.CharField(max_length=200, verbose_name='Search Terms', blank=True, help_text='Enter any abbreviations used for the medication. Ex: HCT, HCTZ for Hydrochlorothiazide')
    base_med_regex = models.CharField(max_length=200, blank=True)
    base_med_pronun = models.CharField(max_length=200, verbose_name='Medication Pronunciation', blank=True)
    base_med_type = models.ManyToManyField('MedType', blank=True, verbose_name='Medication Type')
    base_med_interactions = models.ManyToManyField('MedType', blank=True, verbose_name='Medication Interactions', related_name='med_interactions') 
    base_med_notes = models.CharField(max_length=400, blank=True)

    class Meta:
        ordering = ['base_med_name']

    def save(self, *args, **kwargs):
        self.base_med_name = self.base_med_name.title()
        if self.base_med_add_terms != '':
            if self.base_med_name not in self.base_med_add_terms:
                self.base_med_add_terms = ', '.join((self.base_med_name, self.base_med_add_terms))
        else:
            self.base_med_add_terms = self.base_med_name
        self.base_med_regex = '(\\b'+re.sub(', ','\\\\b|\\\\b',self.base_med_add_terms)+'\\b)'
        related_meds = Medication.objects.filter(Q(med_1 = self) | Q(med_2 = self) | Q(med_3 = self) | Q(med_4 = self))
        for i in related_meds: i.save() 
        super(BaseMed, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.base_med_name.title()}'


        
class Medication(models.Model):
    med_1 = models.ForeignKey(
        BaseMed, 
        blank = True, 
        on_delete=models.CASCADE, 
        related_name='med_1'
        )
    med_2 = models.ForeignKey(
        BaseMed, 
        blank = True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='med_2'
        )
    med_3 = models.ForeignKey(
        BaseMed, 
        blank = True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='med_3'
        )
    med_4 = models.ForeignKey(
        BaseMed, 
        blank = True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='med_4')
    trade_name = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name='Trade Name', 
        help_text='Separate multiple trade names with a comma.  Ex: Advil, Motrin'
        )
    med_qualifiers = models.ManyToManyField(
        'MedQualifier', 
        blank=True, 
        help_text='Select any characteristics specific to this formulation of the  medication. Ex: Extended Release or lotion')
    med_add_terms = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Additional Regular Expression Search Terms", 
        help_text="Add any additional search terms that will help differentiate this medication from other similar medications.  Ex: 25mg for Viagra (Sildenifil), 10mg for Rovatio (Sildenifil)"
        )
    med_pronun = models.CharField(
        max_length=200,
        blank = True,
        verbose_name = "Pronunciation"
        )
    med_route = models.ForeignKey(
        'MedRoute', 
        verbose_name="Medication Route",
        null = True, 
        on_delete=models.CASCADE
        )
    display_name = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Display Name",
        default="",
        help_text="Automatically generated name based on the trade name and generic medications selected."
        )
    custom_disp_name = models.CharField(
        max_length=200, 
        blank=True, 
        default='',
        verbose_name="Custom Trade Name",
        help_text="Enter a different custom name if the autmomatically generated name is not formatted correctly.  Be sure to update if any medications are made to the medications."
        )
    trade_name_regex = models.CharField(
        max_length=200,
        blank=True, 
        default=''
    )
    med_commonuses = models.CharField(
        max_length=200, 
        default="", 
        blank=True,
        verbose_name="Common medication uses", 
        help_text="Add the common uses for this medication. Ex: enter 'Pain' for Tylenol"
        )
    med_notes = models.CharField(
        max_length=200,
        default="", 
        blank=True
        )


    def format_trade_name(self):
        tr_name = self.trade_name.title()
        tr_cap = [
            'lido',
            'derm',
            'oxy',
            'depo',
            'edex',
            'emla',
            'pred',
            'flo',
            'gold',
            'gris',
            'gyne',
            'ifex',
            'tab',
            'klor',
            'levo',
            'low',
            'iron',
            'neo',
            'nor',
            'ogen',
            'olux',
            'orap',
            'alli',
            'plan',
            'qvar',
            'gene',
            'slow',
            'solu',
            'soma',
            'tobi',
            'tri',
            'luma',
            'tev',
            'theo',
            'tao',
            'urex',
            'urso',
            'vira',
            'yaz',
            'vax',
            'ziac',
            'zinc',
            'zmax',
            'acid',
        ]
        tr_join = '|'.join(tr_cap)   
        tr_regex = r'\b(?!(' +tr_join + r'))(\w{1,4})\b'
        tr_matches = re.search(tr_regex, tr_name,re.IGNORECASE)
        if tr_matches:
            for i in tr_matches.groups():
                if i is not None:
                    tr_name = re.sub(r'\b'+i+r'\b',i.upper(),tr_name)
        return tr_name

    def med_type_str(self):
        med_type_list = list()
        for i in (self.med_1, self.med_2, self.med_3, self.med_4):
            if i is not None:
                for j in i.base_med_type.all():
                    med_type_list.append(j.type_name.title())
        if len(med_type_list)>0:
            return ', '.join(med_type_list)

                    



    def set_display_name(self):
        disp_name = f'{self.med_1.base_med_name.title()}'
        if self.med_2:
            disp_name += f'/{self.med_2.base_med_name.title()}'
            if self.med_3:
                disp_name += f'/{self.med_3.base_med_name.title()}'
                if self.med_4:
                    disp_name += f'/{self.med_4.base_med_name.title()}'
        debug_print('len(self.med_qualifiers.all())',len(self.med_qualifiers.all()))
        if len(self.med_qualifiers.all()) >0:
            med_qual = self.med_qualifiers.all()
            for item in med_qual:
                disp_name += f', {item.qual_name}'

        if self.trade_name != '':
            disp_name = f'{self.format_trade_name()} ({disp_name.upper()})'
            
        return disp_name
            
    def set_med_pronun(self):
        pronun_list = [i.base_med_pronun for i in (self.med_1, self.med_2, self.med_3, self.med_4) if i is not None]
        if pronun_list is not None:
            return ' / '.join(pronun_list)

    def set_trade_name_regex(self):
        regex_list = []
        if self.trade_name != "":
            regex_list.append('(\\b'+re.sub(', ','\\\\b|\\\\b',self.trade_name)+'\\b)')
        if self.med_add_terms != '':
            regex_list.append('(\\b'+re.sub(', ','\\\\b|\\\\b',self.trade_name)+'\\b)')
        return '|'.join(regex_list)
            
    @property
    def regex_med_1(self):
        return self.med_1.base_med_regex
    
    @property
    def regex_med_2(self):
        if self.med_2 is not None:
            return self.med_2.base_med_regex           
    
    @property
    def regex_med_3(self):
        if self.med_3 is not None:
            return self.med_3.base_med_regex 

    @property
    def regex_med_4(self):
        if self.med_4 is not None:
            return self.med_4.base_med_regex 

    @property
    def regex_qual(self):
        if self.med_qualifiers.all().count() >0:
            reg_list = []
            for i in self.med_qualifiers.all():
                reg_list.append(MedQualifier.objects.get(qual_name=i).qual_regex)     
            return f'{"|".join(reg_list)}'

    @property
    def regex_route(self):
        return '(\\b'+re.sub(', ','\\\\b|\\\\b',self.med_route.route_regex)+'\\b)' 

    class Meta:
        ordering = ['med_1']

    def get_absolute_url(self):
        return reverse('medrec_v2:med_detail', args=[str(self.id),])

    def rehash_meds(self):
        if re.search('\\\\', self.med_1):
            return True
        else: 
            return False

    def save(self, *args, **kwargs):
        super(Medication, self).save(*args, **kwargs)
        self.display_name = self.set_display_name()
        self.trade_name_regex = self.set_trade_name_regex()
        self.med_pronun = self.set_med_pronun()
        super(Medication, self).save(*args, **kwargs)

    def __str__(self):
        str_1 = f'{self.med_1.base_med_name.title()}'
        if self.med_2 is not None:
            str_1 = f'{"_".join((str_1, self.med_2.base_med_name.title()))}'
        if self.med_3 is not None:
            str_1 = f'{"_".join((str_1, self.med_3.base_med_name.title()))}'
        if self.med_4 is not None:
            str_1 = f'{"_".join((str_1, self.med_4.base_med_name.title()))}'
        if self.med_route is not None:
            str_1 = "_".join((str_1, self.med_route.route_name))
        str_1 = re.sub(' ', '_', str_1)
        return str_1

class MedQualifier(models.Model):
    qual_name = models.CharField(max_length=50)
    qual_desc = models.CharField(max_length=200, blank=True)
    qual_add_terms = models.CharField(max_length=200, blank=True, verbose_name='Additional Search Terms', help_text='Enter any additional search terms for this qualifier')
    qual_regex = models.CharField(max_length=200, blank=True)


    class Meta:
        ordering = ['qual_name']

    def save(self, *args, **kwargs):
        if self.qual_add_terms:
            if self.qual_name.lower() not in self.qual_add_terms.lower():
                self.qual_add_terms = ', '.join((self.qual_add_terms, self.qual_add_terms))
        else: self.qual_add_terms = self.qual_name
        addterm_to_regex = re.sub(r'\\',r'\\', self.qual_add_terms)
        addterm_to_regex = '(\\b' + re.sub(', ','\\\\b|\\\\b', addterm_to_regex) + '\\b)'
        self.qual_regex = addterm_to_regex
        super(MedQualifier, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.qual_name}'

class MedRoute(models.Model):
    route_name = models.CharField(max_length=50)
    route_desc = models.CharField(max_length=200, blank=True)
    route_add_term = models.CharField(max_length=200)
    route_regex = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if self.route_add_term:
            if self.route_name.lower() not in self.route_add_term.lower():
                self.route_add_term = ', '.join((self.route_name, self.route_add_term))
        else: self.route_add_term = self.route_name
        # addterm_to_regex = re.sub('\\','\\',self.route_add_term)
        self.route_regex = '(\\b' + re.sub(', ','\\\\b|\\\\b',self.route_add_term) + '\\b)'
        super(MedRoute, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.route_name}'

class MedType(models.Model):
    type_name = models.CharField(max_length=200)
    type_desc = models.CharField(max_length=200, blank=True)
    type_interact = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f'{self.type_name}'

class MedInput(models.Model):
    med_input = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.id}'
    

@Field.register_lookup
class ReverseRegexIgnoreCase(Lookup):
    lookup_name = 'irevreg'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s REGXEP %s' % (rhs, lhs), params

class SigLookup(models.Model):
    sig_name = models.CharField(max_length=200)
    sig_plain_text = models.CharField(max_length=200)
    sig_add_term = models.CharField(max_length=200)
    sig_regex = models.CharField(max_length=200, blank=True)
    sig_bool = models.BooleanField(verbose_name= "Regex Used")

    def save(self, *args, **kwargs):
        # if self.sig_add_term:
        #     if self.sig_name.lower() not in self.sig_add_term.lower():
        #         self.sig_add_term = ', '.join((self.sig_name, self.sig_add_term))
        # else: self.sig_add_term = self.sig_name
        if self.sig_bool == False:
            self.sig_regex = '(\\b' + re.sub(', ','\\\\b|\\\\b',self.sig_add_term) + '\\b)'
        else:
            self.sig_regex = self.sig_add_term
        super(SigLookup, self).save(*args, **kwargs)

    class Meta:
        ordering=["sig_name"]

    def __str__(self):
        return f'{self.sig_name}'

class DoseLookup(models.Model):
    dose_num = models.IntegerField()
    dose_regex = models.TextField(max_length=1000)

    def __str(self):
        return f'Dose_regex {self.dose_num} '

class DateLookup(models.Model):
    date_num = models.IntegerField()
    date_regex = models.TextField(max_length=1000)

    def __str(self):
        return f'Date_regex {self.date_num}'

class InstLookup(models.Model):
    inst_num = models.IntegerField()
    inst_regex = models.TextField(max_length=1000)

    class Meta:
        ordering = ['inst_num']

    def __str(self):
        return f'Inst_regex {self.inst_num}'


# Create your models here.


def debug_print(text:str, arg, current_frame=currentframe()):
    frame_info = getframeinfo(current_frame)
    file_name = os.path.basename(frame_info.filename)
    print(f'{file_name} ln:{current_frame.f_back.f_lineno} >> {text}: {arg}')
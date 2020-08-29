import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _   
 
class MedRecForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea, help_text="paste in meds from AHLTA")
    
    
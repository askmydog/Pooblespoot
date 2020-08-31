import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _   
 
class MedRecForm(forms.Form):
    query = forms.TextField(widget=forms.Textarea, label='Input Meds Here', help_text="Paste or free-text meds here")
    
    
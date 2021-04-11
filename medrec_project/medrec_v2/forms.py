from medrec_v2.models import Medication, SigLookup
from django import forms

class MedInputForm(forms.Form):

    input_meds = forms.CharField(max_length=1000, label="Medication Input", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['input_meds'].widget.attrs.update({'autofocus':'autofocus'})
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})


class AddMedForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
        # self.fields['generic_name'].widget.attrs.update({"class":"form-control"})
        # self.fields['trade_name'].widget.attrs.update({"class":"form-control"})
        # self.fields['re_match_1'].widget.attrs.update({"class":"form-control"})
        # self.fields['re_match_2'].widget.attrs.update({"class":"form-control"})



class SigForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SigForm, self).__init__(*args, **kwargs)
        self.fields['sig_plain_text'].strip = False

    class Meta:
        model = SigLookup
        fields = "__all__"
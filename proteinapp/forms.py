import math
from django import forms
from django.forms import ModelForm
from .models import Protein

# Create protein form
class ProteinForm(ModelForm):
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'length', 'taxonomy', 'domains']

    # Validate data 
    def clean(self):
        cleaned_data = super(ProteinForm, self).clean()
        protein_id = cleaned_data.get('protein_id')
        sequence = cleaned_data.get('sequence')
        length = cleaned_data.get('length')
        taxonomy = cleaned_data.get('taxonomy')
        domains = cleaned_data.get('domains')

        if not protein_id:
            raise forms.ValidationError("Protein must have protein_id")
        if not sequence:
            raise forms.ValidationError("Protein must have sequence")
        if not length or math.isnan(length):
            raise forms.ValidationError("Protein must have a numeric length")
        return cleaned_data


# class ProteinForm(forms.Form):
#     protein_id = forms.CharField(max_length=60, label='Protein ID')
#     sequence = forms.CharField(max_length=500)
#     length = forms.IntegerField()


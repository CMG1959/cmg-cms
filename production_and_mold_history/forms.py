from django import forms
from production_and_mold_history.models import ProductionHistory, MoldHistory

class phlLookup(forms.Form):
    job_Number = forms.CharField(label="Job Number:",max_length=15)

class moldLookup(forms.Form):
    mold_Number = forms.CharField(label="Number Number:",max_length=10)

class phlForm(forms.ModelForm):
    class Meta:
        model = ProductionHistory
        fields = ['inspectorName', 'jobNumber', 'descEvent' ]

class mhlForm(forms.ModelForm):
    class Meta:
        model = MoldHistory
        fields = ['inspectorName','moldNumber','pm','repair','hours_worked','descEvent']

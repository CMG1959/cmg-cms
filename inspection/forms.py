from django import forms
from inspection.models import partWeightInspection, visualInspection, shotWeightInspection

class jobReportSearch(forms.Form):
    job_Number = forms.CharField(label="Job Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


class itemReportSearch(forms.Form):
    item_Number = forms.CharField(label="Item Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


class partWeightForm(forms.ModelForm):
    class Meta:
        model = partWeightInspection
        fields = ['jobID','machineOperator','inspectorName','headCavID', 'partWeight']


class visualInspectionForm(forms.ModelForm):
    class Meta:
        model = visualInspection
        fields = ['jobID','machineOperator','inspectorName','headCavID', 'inspectionResult', 'defectType']


class shotWeightForm(forms.ModelForm):
    class Meta:
        model = shotWeightInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'shotWeight']

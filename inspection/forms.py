from django import forms
from inspection.models import partWeightInspection, visualInspection

class jobReportSearch(forms.Form):
    job_Number = forms.CharField(label="Job Number:", max_length=15)


class itemReportSearch(forms.Form):
    item_Number = forms.CharField(label="Item Number:", max_length=15)



class partWeightForm(forms.ModelForm):
    class Meta:
        model = partWeightInspection
        fields = ['jobID','machineOperator','inspectorName','headCavID', 'partWeight']


class visualInspectionForm(forms.ModelForm):
    class Meta:
        model = visualInspection
        fields = ['jobID','machineOperator','inspectorName','headCavID', 'inspectionResult', 'defectType']

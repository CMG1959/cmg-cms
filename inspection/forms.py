from django import forms
from inspection.models import passFailInspection, rangeInspection, textInspection


class passFailInspectionForm(forms.ModelForm):
    class Meta:
        model = passFailInspection
        fields = ['passFailTestName','jobID','machineOperator','inspectorName','inspectionResult',
                  'defectType','headCavID']

class rangeInspectionForm(forms.ModelForm):
    class Meta:
        model = rangeInspection
        fields = ['rangeTestName','jobID','machineOperator','inspectorName','isFullShot',
                  'headCavID','numVal','inspectionResult']

class textInspectionForm(forms.ModelForm):
    class Meta:
        model = textInspection
        fields = ['textTestName','jobID','machineOperator','inspectorName','isFullShot','headCavID','inspectionResult']

class jobReportSearch(forms.Form):
    job_Number = forms.CharField(label="Job Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


class itemReportSearch(forms.Form):
    item_Number = forms.CharField(label="Item Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


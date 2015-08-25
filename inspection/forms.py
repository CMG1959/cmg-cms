from django import forms
from inspection.models import passFailInspection, partWeightInspection, visualInspection, shotWeightInspection, outsideDiameterInspection, \
    volumeInspection, neckDiameterInspection, assemblyInspection, cartonTemperature, visionInspection


class passFailInspectionForm(forms.ModelForm):
    class Meta:
        model = passFailInspection
        fields = ['passFailTestName','jobID','machineOperator','inspectorName','inspectionResult',
                  'defectType','headCavID']


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
        fields = ['jobID', 'machineOperator', 'inspectorName', 'headCavID', 'partWeight']


class visualInspectionForm(forms.ModelForm):
    class Meta:
        model = visualInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'headCavID', 'inspectionResult', 'defectType']


class shotWeightForm(forms.ModelForm):
    class Meta:
        model = shotWeightInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'shotWeight']


class outsideDiameterForm(forms.ModelForm):
    class Meta:
        model = outsideDiameterInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'outsideDiameter']


class volumeInspectionForm(forms.ModelForm):
    class Meta:
        model = volumeInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'liquidWeight']


class neckDiameterForm(forms.ModelForm):
    class Meta:
        model = neckDiameterInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'testResult']


class assemblyInspectionForm(forms.ModelForm):
    class Meta:
        model = assemblyInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'assemblyTestResults']


class cartonTempForm(forms.ModelForm):
    class Meta:
        model = cartonTemperature
        fields = ['jobID', 'machineOperator', 'inspectorName', 'cartonTemp']


class visionInspectionForm(forms.ModelForm):
    class Meta:
        model = visionInspection
        fields = ['jobID', 'machineOperator', 'inspectorName', 'visionTestResults']

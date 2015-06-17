from django import forms
from django.forms.util import flatatt
from inspection.models import partWeightInspection, visualInspection
from employee.models import employee

class partWeightForm(forms.ModelForm):
    class Meta:
        model = partWeightInspection
        fields = ['jobID','machineOperator','inspectorName','dateCreated',
                  'cavityID','partWeight']


class visualInspectionForm(forms.ModelForm):
    class Meta:
        model = visualInspection
        fields = ['jobID','machineOperator','inspectorName','dateCreated',
                  'cavityID','inspectionResult','defectType']

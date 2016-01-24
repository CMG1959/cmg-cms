from django import forms
from inspection.models import passFailInspection, rangeInspection, textInspection, IntegerInspection, FloatInspection
from django.core.validators import RegexValidator
import re


class passFailInspectionForm(forms.ModelForm):
    class Meta:
        model = passFailInspection
        fields = ['passFailTestName','jobID','machineOperator','inspectionResult',
                  'defectType','headCavID']


class rangeInspectionForm(forms.ModelForm):
    class Meta:
        model = rangeInspection
        fields = ['rangeTestName','jobID','machineOperator','isFullShot',
                  'headCavID','numVal']

class textInspectionForm(forms.ModelForm):
    class Meta:
        model = textInspection
        fields = ['textTestName','jobID','machineOperator','isFullShot','headCavID','inspectionResult']

class IntegerInspectionForm(forms.ModelForm):
    class Meta:
        model = IntegerInspection
        fields = ['integerTestName','jobID','machineOperator','isFullShot','headCavID','inspectionResult']

class FloatInspectionForm(forms.ModelForm):
    class Meta:
        model = FloatInspection
        fields = ['floatTestName','jobID','machineOperator','isFullShot','headCavID','inspectionResult']


class jobReportSearch(forms.Form):
    CHOICES=[('htmlReport','Web'),
         ('pdfReport','PDF')]
    report_type = forms.ChoiceField(label='Report Type', choices=CHOICES, widget=forms.RadioSelect())
    job_Number = forms.CharField(label="Job Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


class itemReportSearch(forms.Form):
    item_Number = forms.CharField(label="Item Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


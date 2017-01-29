from django import forms
from inspection.models import passFailInspection, numericInspection, textInspection,  RangeInspection #IntegerInspection,
from django.core.validators import RegexValidator
import re
from cav_builder import get_inspection_type, get_qms_insp_def

def build_cavs(cavs_str):
    cavs_array = cavs_str.split('~')
    return [(x,x) for x in cavs_array]

def build_defects(defect_str):
    defect_array = []
    for each_item in defect_str.split('~'):
        match = re.search('\[(?P<defect_key>\d+)\] (?P<defect_str>.*)', each_item)
        if match:
            defect_array.append((match.group('defect_key'), match.group('defect_str')))
    return defect_array

def build_inspection_fields(job_id, inspection_type, inspection_id, man_num):
    inspection_type_int = get_inspection_type(inspection_type)
    built_inspection = get_qms_insp_def(job_id=job_id, inspection_type=inspection_type_int,
                                        inspection_id=inspection_id, man_num=man_num)
    if inspection_type in ['Pass/Fail','Pass-Fail']:
        headCavID_fields = build_cavs(built_inspection['Cavs_Array'])
        defectType_fields = build_defects(built_inspection['Critera_Array'])
        return headCavID_fields, defectType_fields

    if inspection_type in ['Range', 'Text', 'Float', 'Integer', 'Numeric', 'NumericVF']:
        headCavID_fields = build_cavs(built_inspection['Cavs_Array'])
        return headCavID_fields, False

    else:
        return False, False






class PassFailIns(forms.ModelForm):
    class Meta:
        model = passFailInspection
        fields = ['machineOperator','inspectionResult',
                  'defectType','headCavID']
        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }


class NumericInspectionForm(forms.ModelForm):
    class Meta:
        model = numericInspection
        fields = ['machineOperator','isFullShot',
                  'headCavID','numVal_1']
        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }


class TextIns(forms.ModelForm):
    class Meta:
        model = textInspection
        fields = ['machineOperator','isFullShot','headCavID','inspectionResult']
        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }


# class IntIns(forms.ModelForm):
#     class Meta:
#         model = IntegerInspection
#         fields = ['machineOperator','isFullShot','headCavID','inspectionResult']
#         widgets = {
#             'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
#         }


class RangeInspectionForm(forms.ModelForm):
    class Meta:
        model = RangeInspection
        fields = ['machineOperator','isFullShot','headCavID','inspectionResult', 'numVal_1', 'numVal_2']
        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }


####
# Old forms here
####


class passFailInspectionForm(forms.ModelForm):
    class Meta:
        model = passFailInspection
        fields = ['passFailTestName','jobID','machineOperator','inspectionResult',
                  'defectType','headCavID']
        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }


class numericInspectionForm(forms.ModelForm):
    class Meta:
        model = numericInspection
        fields = ['numericTestName','jobID','machineOperator','isFullShot',
                  'headCavID','numVal_1']

        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }


class textInspectionForm(forms.ModelForm):
    class Meta:
        model = textInspection
        fields = ['textTestName','jobID','machineOperator','isFullShot','headCavID','inspectionResult']
        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }


# class IntegerInspectionForm(forms.ModelForm):
#     class Meta:
#         model = IntegerInspection
#         fields = ['integerTestName','jobID','machineOperator','isFullShot','headCavID','inspectionResult']
#         widgets = {
#             'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
#         }


class rangeInspectionForm(forms.ModelForm):
    class Meta:
        model = RangeInspection
        fields = ['rangeTestName','jobID','machineOperator','isFullShot','headCavID','inspectionResult','numVal_1', 'numVal_2']
        widgets = {
            'headCavID': forms.Select(attrs={'class':'select'}, choices=[(-1,-1)])
        }




class jobReportSearch(forms.Form):
    CHOICES=[('htmlReport','Web'),
             ('htmlReport_noplot','Web (no charts)'),
         ('pdfReport','PDF')]
    report_type = forms.ChoiceField(label='Report Type', choices=CHOICES, widget=forms.RadioSelect())
    job_Number = forms.CharField(label="Job Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


class itemReportSearch(forms.Form):
    item_Number = forms.CharField(label="Item Number:", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)



'''
FORMS WITH VARYING NUMBER OF FIELDS
Reference: https://jacobian.org/writing/dynamic-form-generation/
'''


class NumericInspectionFormVF(forms.Form):
    is_full_shot = forms.BooleanField(label='Is Full Shot?', required=False)
    machine_operator = forms.CharField(label='Machine Operator')

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(NumericInspectionFormVF, self).__init__(*args, **kwargs)

        for i, cavity_id in enumerate(extra):
            if cavity_id == '-':
                self.fields['cav_%s' % i] = forms.DecimalField(label='Full Shot', required=False)
            else:
                self.fields['cav_%s' % i] = forms.DecimalField(label='Cav %s'% cavity_id, required=False)


    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('cav_'):
                yield (self.fields[name].label, value)
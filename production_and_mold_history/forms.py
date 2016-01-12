from django import forms
from production_and_mold_history.models import ProductionHistory, MoldHistory
from employee.models import Employees

class phlLookup(forms.Form):
    choices = (
        ('Job Number', 'Job Number'),
        ('Mold Number','Mold Number')
    )
    item_type = forms.ChoiceField(choices=choices, label='Search Type')
    id_Number = forms.CharField(label="ID", max_length=15)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)


class moldLookup(forms.Form):
    mold_Number = forms.CharField(label="Mold Number:", max_length=10)
    date_from = forms.DateField(label="Date From:", required=False)
    date_to = forms.DateField(label="Date To:", required=False)

class moldLookupForm(forms.Form):
    mold_Number = forms.CharField(label="Mold Number:", max_length=10)

class phlForm(forms.ModelForm):
    class Meta:
        model = ProductionHistory
        fields = ['inspectorName', 'descEvent','notifyToolroom']


class mhlForm(forms.Form):
    Date_Performed = forms.DateField(label="Date Performed", required=True)
    inspectorName = forms.ModelChoiceField(queryset=Employees.objects.filter(StatusActive=True,
                                                                         IsToolStaff=True).order_by('EmpLName'),
                                           label="Name", required=True)
    pm = forms.BooleanField(label="Preventative Maintenance", required=False)
    repair = forms.BooleanField(label="Repair", required=False)
    hours_worked = forms.DecimalField(label="Hours worked",decimal_places=2, max_digits=10, min_value=0, required=True)
    descEvent = forms.CharField(label="Event Description",max_length=1000, required=True)
    # class Meta: ##
    #     model = MoldHistory
    #     fields = ['inspectorName', 'pm', 'repair', 'hours_worked', 'descEvent']

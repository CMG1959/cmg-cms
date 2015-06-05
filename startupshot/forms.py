from django import forms
from startupshot.models import CIMC_Production

class startupShotLookup(forms.Form):
    part_Number = forms.CharField(label="Part Number:",max_length=10)


class startupShotForm(forms.ModelForm):
    class Meta:
        model = CIMC_Production
        fields = ['item','jobNumber','partWeight','cavityID','headID','activeCavities','dateCreated']


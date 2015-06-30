from django import forms
from startupshot.models import startUpShot

class startupShotLookup(forms.Form):
    part_Number = forms.CharField(label="Part Number:",max_length=10)


class startupShotForm(forms.ModelForm):
    class Meta:
        model = startUpShot
        fields = ['inspectorName', 'shotWeight', ]

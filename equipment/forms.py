from django import forms
from equipment.models import EquipmentPM


class equipmentPMForm(forms.ModelForm):
    class Meta:
        model = EquipmentPM
        fields = ['employee', 'logged_pm', ]

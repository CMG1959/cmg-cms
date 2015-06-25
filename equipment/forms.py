from django import forms
from equipment.models import EquipmentPM


class equipmentPMForm(forms.ModelForm):
    class Meta:
        model = EquipmentPM
        fields = ['employee', 'equipment_ID', 'pm_frequency', 'logged_pm']

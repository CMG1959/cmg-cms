from django import forms
from equipment.models import EquipmentPM, EquipmentRepair


class equipmentPMForm(forms.ModelForm):
    class Meta:
        model = EquipmentPM
        fields = ['employee', 'equipment_ID', 'pm_frequency', 'logged_pm','comments']


class equipmentRepairForm(forms.ModelForm):
    class Meta:
        model = EquipmentRepair
        fields = ['employee', 'equipment_ID', 'po_num', 'part_supplier', 'part_name', 'part_number', 'part_cost',
                  'part_quantity','comments']

from django import forms
from equipment.models import EquipmentPM, EquipmentRepair


class equipmentPMForm(forms.ModelForm):
    class Meta:
        model = EquipmentPM
        fields = ['Date_Performed',  'equipment_ID', 'pm_frequency', 'logged_pm','comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows':10, 'spellcheck': True}),
        }



class equipmentRepairForm(forms.ModelForm):
    class Meta:
        model = EquipmentRepair
        fields = ['Date_Performed', 'equipment_ID', 'po_num', 'part_supplier', 'part_name', 'part_number', 'part_cost',
                  'part_quantity','comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows':10, 'spellcheck': True}),
        }
from django import forms
from equipment.models import EquipmentPM, EquipmentRepair


class equipmentPMForm(forms.ModelForm):
    class Meta:
        model = EquipmentPM
        fields = ['Date_Performed',  'equipment_ID', 'pm_frequency', 'logged_pm','comments']

    def __init__(self, *args, **kwargs):
        super(equipmentPMForm, self).__init__(*args, **kwargs)
        self.fields['comments'].widget.attrs['rows'] = 4


class equipmentRepairForm(forms.ModelForm):
    class Meta:
        model = EquipmentRepair
        fields = ['Date_Performed', 'equipment_ID', 'po_num', 'part_supplier', 'part_name', 'part_number', 'part_cost',
                  'part_quantity','comments']

    def __init__(self, *args, **kwargs):
            super(equipmentRepairForm, self).__init__(*args, **kwargs)
            self.fields['comments'].widget.attrs['rows'] = 4
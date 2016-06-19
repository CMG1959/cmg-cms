from django import forms
from .models import *


class FormPropNumericlimit(forms.ModelForm):
    class Meta:
        model = PropNumericLimit
        fields = ['prop_value','cav_id',
                  'head_id']

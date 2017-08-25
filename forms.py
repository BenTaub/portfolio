from django import forms
from django.forms import ModelForm

from balancer.models import SecuritiesAvail


# from django.forms import modelformset_factory, formset_factory

class ManageSecurity(ModelForm):
    """Used to add and manage securities"""

    class Meta:
        model = SecuritiesAvail
        fields = ['id', 'name', 'symbol', 'price']
        widgets = {'id': forms.HiddenInput, 'name': forms.TextInput, 'symbol': forms.TextInput,
                   'price': forms.NumberInput}

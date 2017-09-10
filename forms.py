from django import forms
from django.forms import ModelForm

from balancer.models import SecurityAvail


# from django.forms import modelformset_factory, formset_factory

class ManageSecurity(ModelForm):
    """Used to add and manage securities"""

    class Meta:
        model = SecurityAvail
        fields = ['security_avail_static', 'id', 'name', 'symbol', 'price', 'at_dt']
        widgets = {'security_avail_static': forms.HiddenInput, 'id': forms.HiddenInput, 'name': forms.TextInput,
                   'symbol': forms.TextInput, 'price': forms.NumberInput, 'at_dt': forms.DateTimeInput}

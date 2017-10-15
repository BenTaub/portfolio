from django import forms
from django.forms import ModelForm

from balancer.models import Account


class FormManageSecurity(forms.Form):
    # Used to edit a security
    id = forms.IntegerField(widget=forms.HiddenInput)
    symbol = forms.CharField(max_length=10, min_length=1, required=False)
    name = forms.CharField(max_length=20, required=True)
    # TODO: Make this a big field for entry but only 50 chars for list display - see old project for direction
    notes = forms.CharField(widget=forms.Textarea, required=False)


class FormAddSecurity(FormManageSecurity):
    """Used when we are adding a new security"""
    def __init__(self, *args, **kwargs):
        super(FormManageSecurity, self).__init__(*args, **kwargs)
        self.fields.pop('id')


FormSetSecurities = forms.formset_factory(FormManageSecurity, extra=0, can_delete=False)


class FormSecurityPrice(forms.Form):
    # Used to record the price of a security at a point in time
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    security_id = forms.IntegerField(widget=forms.HiddenInput)
    symbol = forms.CharField(max_length=10, min_length=1, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'readonly': 'readonly', 'outline': 'none'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), required=False)
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'step': '0.01', 'max': '999999',
                                                               'text-align': 'right;'}))
    price_dt = forms.DateField(widget=forms.HiddenInput)


FormSetSecurityPrices = forms.formset_factory(FormSecurityPrice, extra=0, can_delete=False)


class FormAccount(ModelForm):
    class Meta:
        model = Account
        fields = ['id', 'name', 'institution', 'acct_num', 'open_dt', 'close_dt', 'notes']
        widgets = {'name': forms.TextInput, 'institution': forms.TextInput, 'acct_num': forms.TextInput,
                   # 'open_dt': forms.TextInput(attrs={'type': 'date'}), 'close_dt': forms.SelectDateWidget}
                   'open_dt': forms.TextInput(attrs={'type': 'date'}),
                   'close_dt': forms.TextInput(attrs={'type': 'date'})}

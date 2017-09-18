from django import forms


# from django.forms import modelformset_factory, formset_factory

# class FormManageSecurity(ModelForm):
#     """Used to add and manage securities"""
#
#     class Meta:
#         model = SecurityAvailDynamic
#         fields = ['security_avail_static', 'id', 'name', 'symbol', 'price', 'at_dt']
#         widgets = {'security_avail_static': forms.HiddenInput(), 'id': forms.HiddenInput(), 'name': forms.TextInput(),
#                    'symbol': forms.TextInput(), 'price': forms.NumberInput(), 'at_dt': forms.DateTimeInput()}

class FormManageSecurity(forms.Form):
    # Used to edit a contact
    id = forms.IntegerField(widget=forms.HiddenInput)
    security_avail_static_id = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField(max_length=20, required=True)
    symbol = forms.CharField(max_length=10, min_length=1, required=False)
    notes = forms.CharField()


class FormAddSecurity(FormManageSecurity):
    """Used when we are adding a new security"""

    def __init__(self, *args, **kwargs):
        super(FormManageSecurity, self).__init__(*args, **kwargs)
        self.fields.pop('security_avail_static_id')
        self.fields.pop('id')


FormSetSecurities = forms.formset_factory(FormManageSecurity, extra=0, )

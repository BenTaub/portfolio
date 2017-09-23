from django import forms


class FormManageSecurity(forms.Form):
    # Used to edit a contact
    id = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField(max_length=20, required=True)
    symbol = forms.CharField(max_length=10, min_length=1, required=False)
    # TODO: Make this a big field for entry but only 50 chars for list display - see old project for direction
    notes = forms.CharField()


class FormAddSecurity(FormManageSecurity):
    """Used when we are adding a new security"""
    def __init__(self, *args, **kwargs):
        super(FormManageSecurity, self).__init__(*args, **kwargs)
        self.fields.pop('id')


FormSetSecurities = forms.formset_factory(FormManageSecurity, extra=0, can_delete=False)

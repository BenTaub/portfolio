from django import forms


class FormManageSecurity(forms.Form):
    # Used to edit a contact
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
    id = forms.IntegerField(widget=forms.HiddenInput)
    symbol = forms.CharField(max_length=10, min_length=1, required=False)
    name = forms.CharField(max_length=20, required=True)
    at_dt = forms.DateTimeField()
    notes = forms.CharField(widget=forms.Textarea, required=False)

# TODO: SCREEN WITH DATE FIELD + EACH SECURITY W/ PRICE AND NOTES (set_security_prices.html)
# TODO: SCREEN FOR ONE SECURITY LISTING ALL PAST DATES, PRICES, & NOTES (security_price_history.html)

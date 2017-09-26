from django import forms
from django.db import models, transaction


class Security(models.Model):
    """
    Each record in this table represents one available security at a point in time
    """
    name = models.TextField()
    symbol = models.TextField(unique=True)
    notes = models.TextField(blank=True, null=True)
    # TODO: Add an 'active' flag - if inactive, don't show on pricing screens
    effective_dt = models.DateTimeField(verbose_name="Record effective date", auto_now=True,
                                        help_text="The date & time on which this record became active")


class SecurityPrice(models.Model):
    """
    Each record in this table represents the price for one available security at a point in time
    """
    security = models.ForeignKey(to=Security)
    # The date & time for this price
    at_dt = models.DateField(verbose_name="Price Date", auto_now_add=True)
    # at_dt = models.DateTimeField(verbose_name="Price Date & Time", default=django.utils.timezone.now)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    effective_dt = models.DateTimeField(verbose_name="Record effective date", auto_now=True,
                                        help_text="The date & time on which this record became active")

    class Meta:
        unique_together = (('security', 'at_dt'),)


def store_formset_in_db(formset: forms.BaseFormSet, db_model, ignore_in_form: list = None,
                        map_model_to_form: dict = None):
    """
    Takes the data from a formset & stores it in a model table. Maps form fields to model fields based on field names.
    map_form_to_model param accomodates name differences if necessary.
    :param formset: The formset containing the data you want to put into the DB
    :param db_model: The model into which you want to store the data
    :param ignore_in_form: Indicates which form fields not to put into the DB.
    :param map_form_to_model: maps form field names to model field names as follows form_field_name:model_field_name
    :return:
    """
    with transaction.atomic():  # Starts a transaction
        for one_form in formset:
            store_form_in_db(form=one_form, db_model=db_model, ignore_in_form=ignore_in_form,
                             map_model_to_form=map_model_to_form, commit_fg=False)
    return


def store_form_in_db(form: forms.BaseForm, db_model, ignore_in_form: list = None, map_model_to_form: dict = None,
                     commit_fg: bool = True):
    """
    Takes the data from a formset & stores it in a model table. Maps form fields to model fields based on field names.
    map_model_to_form param accomodates name differences if necessary.
    NOTE: This function loops through the fields available in the model object. Thus, if the form contains fields not
    in the model, they are ignored.
    :param form: The form containing the data you want to put into the DB
    :param db_model: The model into which you want to store the data
    :param ignore_in_form: Indicates which form fields not to put into the DB.
    :param map_model_to_form: maps form field names to model field names as follows form_field_name:model_field_name
    :param commit_fg: Determines whether this function should issue a commit or not
    :return:
    """

    def insert_rec():
        """
        actually inserts data in the db
        """
        new_rec = db_model()
        for field in new_rec.__dict__:
            if field in ignore_in_form:
                continue
            elif field in form.cleaned_data:
                setattr(new_rec, field, form.cleaned_data[field])
            elif field in map_model_to_form:
                setattr(new_rec, field, form.cleaned_data[map_model_to_form[field]])
        new_rec.save()

    if commit_fg:
        with transaction.atomic():
            insert_rec()
    else:
        insert_rec()

    return

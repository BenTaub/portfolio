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
    price_dt = models.DateField(verbose_name="Price Date")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    effective_dt = models.DateTimeField(verbose_name="Record effective date",
                                        help_text="The date & time on which this record became active",
                                        auto_now=True)

    class Meta:
        unique_together = (('security', 'price_dt'),)


def dictfetchall(cursor):
    """
    Gets all the rows from a cursor and returns then in a list of dicts. Each rec is a db rec and each key is
    the related column name
    :param cursor: A Django cursor
    :return:
    """
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def store_formset_in_db(formset: forms.BaseFormSet, db_model):
    """
    Takes the data from a formset & stores it in a model table. Maps form fields to model fields based on field names.
    map_form_to_model param accomodates name differences if necessary.
    :param formset: The formset containing the data you want to put into the DB
    :param db_model: The model into which you want to store the data
    :return:
    """
    with transaction.atomic():  # Starts a transaction
        for one_form in formset:
            store_form_in_db(form=one_form, db_model=db_model, commit_fg=False)
    return


def store_form_in_db(form: forms.BaseForm, db_model, commit_fg: bool = True):
    """
    Takes the data from a formset & stores it in a model table. Maps form fields to model fields based on field names.
    NOTE: This function loops through the fields available in the model object. Thus, if the form contains fields not
    in the model, they are ignored.
    :param form: The form containing the data you want to put into the DB
    :param db_model: The model into which you want to store the data
    :param commit_fg: Determines whether this function should issue a commit or not
    :return:
    """

    def insert_rec():
        """
        actually inserts data in the db
        """
        if not form.has_changed():
            return
        new_rec = db_model()
        for field in new_rec.__dict__:
            if field in form.cleaned_data:
                setattr(new_rec, field, form.cleaned_data[field])
        # # TODO: Modify this to put errors on each record that has an error
        new_rec.save()

    if commit_fg:
        with transaction.atomic():
            insert_rec()
    else:
        insert_rec()

    return

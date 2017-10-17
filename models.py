import django.utils.timezone
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

    def __str__(self): return self.symbol + ': ' + self.name


class SecurityPrice(models.Model):
    """
    Each record in this table represents the price for one available security at a point in time
    """
    security = models.ForeignKey(to=Security)
    price_dt = models.DateField(verbose_name="Price Date")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    effective_dt = models.DateTimeField(verbose_name="Record effective date",
                                        help_text="The date & time on which this record became active",
                                        auto_now=True)

    class Meta:
        unique_together = (('security', 'price_dt'),)


class Account(models.Model):
    """
    Each record represents an account that contains shares or other holdings
    """
    name = models.TextField()
    institution = models.TextField(verbose_name='Financial Institution', blank=True)
    acct_num = models.TextField(verbose_name='Account Number', blank=True)
    notes = models.TextField(blank=True, null=True)
    open_dt = models.DateField(verbose_name='Open Date', blank=True, null=True)
    close_dt = models.DateField(verbose_name='Close Date', blank=True, null=True)
    effective_dt = models.DateTimeField(verbose_name="Record effective date",
                                        help_text="The date & time on which this record became active",
                                        auto_now=True)

    def __str__(self): return self.name


class Holding(models.Model):
    """Each record represents one security held in an account at a point in time"""
    asset = models.ForeignKey(to=Security)
    account = models.ForeignKey(to=Account, blank=True, null=True)  # Assets aren't necessarily in an account
    notes = models.TextField(blank=True, null=True)
    num_shares = models.DecimalField(decimal_places=2, max_digits=8)  # A negative amount refers to a liability
    as_of_dt = models.DateField(verbose_name='As Of',
                                default=django.utils.timezone.now)  # The date on which this # of shares started to apply
    effective_dt = models.DateTimeField(verbose_name="Record effective date",
                                        help_text="The date & time on which this record became active",
                                        auto_now=True)

    class Meta:
        unique_together = (('asset', 'account', 'as_of_dt'),)

    def save(self, *args, **kwargs):
        # NOTE: Intention of this approach is to update existing records & insert new ones, putting the record ID
        # on the rec used in the original save call - I tested it and it seems to work

        # Query Holding the date - acct - security combination on curr rec
        # If it exists, take its ID and put it on the current record - this should force an update
        test_rec = Holding.objects.filter(as_of_dt__exact=self.as_of_dt, account__exact=self.account,
                                          asset__exact=self.asset)

        # DB constraint should protect against getting more than one rec so not testing for that
        if test_rec.exists():
            self.id = test_rec.values()[0]['id']
        else:
            self.id = None
        # If not, remove id from the current record - this should force an insert
        super(Holding, self).save(*args, **kwargs)  # Call the "real" save() method.


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

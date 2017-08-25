import datetime

import django.utils.timezone
from django.db import models, transaction, Error


# Create your models here.
class SecuritiesAvail(models.Model):
    name = models.TextField()
    symbol = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    current_rec_fg = models.BooleanField(verbose_name="Current record flag", default=True,
                                         help_text="Set to True for the current version of the record")
    effective_dt = models.DateTimeField(verbose_name="Record effective date", default=django.utils.timezone.now,
                                        help_text="The date & time on which this record became active")
    end_dt = models.DateTimeField(verbose_name="Record end date",
                                  help_text="The date and time on which this record expired", blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        """
        Overrides the parent class' delete method as all contact deletes will be logical
        :param using:
        :param keep_parents:
        :return:
        """
        curr_datetime = datetime.datetime.now()
        try:
            with transaction.atomic():  # Starts a transaction
                # Logically delete the dynamic record
                self.end_dt = curr_datetime
                self.current_rec_fg = False
                self.save(force_update=True)
        except Error as db_err:
            # TODO: Do something here!!!
            print(str(db_err))

            # TODO: Need to redefine 'get' method to always go where current_rec_fg == True

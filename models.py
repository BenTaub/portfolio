import datetime

import django.utils.timezone
from django.db import models, transaction, Error


# Create your models here.
class SecurityAvailStatic(models.Model):
    """
    This is info about an available security that never changes and serves as a place on which to build relationships
    For the time being, the only field on this table is the table key

    """
    curr_rec_fg = models.BooleanField(verbose_name="Current record flag", default=True,
                                      help_text="Set to True for the current version of the record")
    effective_dt = models.DateTimeField(verbose_name="Record effective date", default=django.utils.timezone.now,
                                        help_text="The date & time on which this record became active")
    end_dt = models.DateTimeField(verbose_name="Record end date",
                                  help_text="The date and time on which this record expired", blank=True, null=True)


class SecurityAvail(models.Model):
    """
    Each record in this table represents one available security at a point in time
    """
    security_avail_static = models.ForeignKey(to=SecurityAvailStatic, blank=True, null=True)
    name = models.TextField()
    symbol = models.TextField()

    # The date & time for this price
    at_dt = models.DateTimeField(verbose_name="Price Date & Time", default=datetime.datetime.now())
    price = models.DecimalField(max_digits=8, decimal_places=2)
    current_rec_fg = models.BooleanField(verbose_name="Current record flag", default=True,
                                         help_text="Set to True for the current version of the record")
    effective_dt = models.DateTimeField(verbose_name="Record effective date", default=django.utils.timezone.now,
                                        help_text="The date & time on which this record became active")
    end_dt = models.DateTimeField(verbose_name="Record end date",
                                  help_text="The date and time on which this record expired", blank=True, null=True)

    def create(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Overrides the parent class' save method
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        curr_datetime = datetime.datetime.now()
        try:
            with transaction.atomic():  # Starts a transaction
                security = SecurityAvailStatic(effective_dt=curr_datetime, curr_rec_fg=True)
                security.save()
                self.security_avail_static = security
                # self.security_static = security
                self.save()
                # super(PersonDynamic, self).save(self)
        except Error as db_err:
            # TODO: Do something here!!!
            print(str(db_err))

    def delete(self, using=None, keep_parents=False):
        """
        Overrides the parent class' delete method as all contact deletes will be logical
        :param using:
        :param keep_parents:
        :return:
        """
        # TODO: Change this to logically delete the parent, too - is delete something we'll really do?
        curr_datetime = datetime.datetime.now()
        try:
            with transaction.atomic():  # Starts a transaction
                # Logically delete the record
                self.end_dt = curr_datetime
                self.current_rec_fg = False
                self.save(force_update=True)
                self.security_avail_static.end_dt = curr_datetime
                self.security_avail_static.curr_rec_fg = False
                self.security_avail_static.save(force_update=True)
        except Error as db_err:
            # TODO: Do something here!!!
            print(str(db_err))

    # TODO: Redefine 'get' method to always go where current_rec_fg == True???

    def update(self):
        # TODO: Does this still work?
        """Provides a way to do an update of a security while keeping history"""
        curr_datetime = datetime.datetime.now()
        try:
            with transaction.atomic():  # Starts a transaction
                # Logically delete the current record
                self.end_dt = curr_datetime
                self.current_rec_fg = False
                self.save(force_update=True)
                self.end_dt = None
                self.current_rec_fg = True
                self.save(force_insert=True)
        except Error as db_err:
            # TODO: Do something here!!!
            print(str(db_err))

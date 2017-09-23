import django.utils.timezone
from django.db import models


#
#
# # Create your models here.
# class SecurityAvailStatic(models.Model):
#     """
#     This is info about an available security that never changes and serves as a place on which to build relationships
#     For the time being, the only field on this table is the table key
#
#     """
#     curr_rec_fg = models.BooleanField(verbose_name="Current record flag", default=True,
#                                       help_text="Set to True for the current version of the record")
#     effective_dt = models.DateTimeField(verbose_name="Record effective date", default=django.utils.timezone.now,
#                                         help_text="The date & time on which this record became active")
#     end_dt = models.DateTimeField(verbose_name="Record end date",
#                                   help_text="The date and time on which this record expired", blank=True, null=True)


class Security(models.Model):
    """
    Each record in this table represents one available security at a point in time
    """
    # security_avail_static = models.ForeignKey(to=SecurityAvailStatic)
    name = models.TextField()
    symbol = models.TextField()
    notes = models.TextField(blank=True, null=True)
    curr_rec_fg = models.BooleanField(verbose_name="Current record flag", default=True,
                                      help_text="Set to True for the current version of the record")
    effective_dt = models.DateTimeField(verbose_name="Record effective date", default=django.utils.timezone.now,
                                        help_text="The date & time on which this record became active")
    end_dt = models.DateTimeField(verbose_name="Record end date",
                                  help_text="The date and time on which this record expired", blank=True, null=True)

    # def create(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     """
    #     Overrides the parent class' save method
    #     :param force_insert:
    #     :param force_update:
    #     :param using:
    #     :param update_fields:
    #     :return:
    #     """
    #     curr_datetime = datetime.datetime.now()
    #     try:
    #         with transaction.atomic():  # Starts a transaction
    #             security = SecurityAvailStatic(effective_dt=curr_datetime, curr_rec_fg=True)
    #             security.save()
    #             self.security_avail_static = security
    #             # self.security_static = security
    #             self.save()
    #             # super(PersonDynamic, self).save(self)
    #     except Error as db_err:
    #         # TODO: Do something here!!!
    #         print(str(db_err))
    #
    # def delete(self, using=None, keep_parents=False):
    #     """
    #     Overrides the parent class' delete method as all contact deletes will be logical
    #     :param using:
    #     :param keep_parents:
    #     :return:
    #     """
    #     curr_datetime = datetime.datetime.now()
    #     try:
    #         with transaction.atomic():  # Starts a transaction
    #             # Logically delete the record
    #             self.end_dt = curr_datetime
    #             self.curr_rec_fg = False
    #             self.save(force_update=True)
    #             self.security_avail_static.end_dt = curr_datetime
    #             self.security_avail_static.curr_rec_fg = False
    #             self.security_avail_static.save(force_update=True)
    #     except Error as db_err:
    #         # TODO: Do something here!!!
    #         print(str(db_err))
    #
    #
    # def update(self, old_ver: object):
    #     """
    #     Does a logical update in which the old version of the record is logically deleted
    #     and a new version is inserted into the table
    #     :param old_ver: A Security object
    #     :return:
    #     """
    #     # TODO: Does this still work?
    #     """Provides a way to do an update of a security while keeping history"""
    #     curr_datetime = datetime.datetime.now()
    #     try:
    #         with transaction.atomic():  # Starts a transaction
    #             # Logically delete the old record
    #             old_ver.end_dt = curr_datetime
    #             old_ver.current_rec_fg = False
    #             old_ver.save(force_update=True, update_fields=['end_dt', 'curr_rec_fg'])
    #
    #             # Insert the new version
    #             self.end_dt = None
    #             self.curr_rec_fg = True
    #             self.save(force_insert=True)
    #     except Error as db_err:
    #         # TODO: Do something here!!!
    #         print(str(db_err))


class SecurityPrice(models.Model):
    """
    Each record in this table represents the price for one available security at a point in time
    """
    security = models.ForeignKey(to=Security)
    # The date & time for this price
    at_dt = models.DateTimeField(verbose_name="Price Date & Time", default=django.utils.timezone.now)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    curr_rec_fg = models.BooleanField(verbose_name="Current record flag", default=True,
                                      help_text="Set to True for the current version of the record")
    effective_dt = models.DateTimeField(verbose_name="Record effective date", default=django.utils.timezone.now,
                                        help_text="The date & time on which this record became active")
    end_dt = models.DateTimeField(verbose_name="Record end date",
                                  help_text="The date and time on which this record expired", blank=True, null=True)

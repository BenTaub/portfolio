from django.db import models


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


def store_formset_in_db(formset: dict, model: models):
    print(str(formset), '\n\n', str(model))
    pass

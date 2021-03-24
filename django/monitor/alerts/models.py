from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars


class AbstractAlert(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    json = models.TextField(blank=False, help_text="RAW json as received by the webhook")

    class Meta:
        abstract = True

    @property
    def short_json(self):
        return "%s..." % truncatechars(self.json, 70)


class GenericAlert(AbstractAlert):
    
    class Meta:
        verbose_name = "Unknown alert"
        verbose_name_plural = "Unknown alerts"

# Create your models here.
class InstanceDownAlert(AbstractAlert):

    STATUS = [
        (0, 'unknown'),
        (1, 'resolved'),
        (2, 'firing'),
    ]

    SEVERITY = [
        (0, 'unknown'),
        (1, 'warning'),
        (2, 'critical'),
    ]

    user = models.ForeignKey(
        User,
        null=True,
        on_delete = models.CASCADE,
        related_name = "alerts",
        related_query_name = "alert",
    )

    status = models.IntegerField(choices=STATUS)
    severity = models.IntegerField(choices=SEVERITY)

    startsAt = models.DateTimeField(null=False)
    endsAt = models.DateTimeField(null=True, blank=True)

    instance = models.TextField(null=True)
    summary = models.TextField(null=True)
    description = models.TextField(null=True)

    @property
    def duration(self):
        return this.endsAt - this.startsAt

    class Meta:
        verbose_name = "Instance down alert"
        verbose_name_plural = "Instance down alerts"


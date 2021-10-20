from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Application(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "applications",
    )
    title = models.CharField(max_length=128, blank=False)
    enable_public_status = models.BooleanField(default=False)

    def is_healthy(self):
        return not self.services.filter(instancedownalerts__status=2)

    def is_critical(self):
        return self.services.filter(instancedownalerts__status=2, is_critical=True)

    def is_warning(self):
        return self.services.filter(instancedownalerts__status=2, is_critical=False)

    def availability(self, days=7):

        from alerts.models import InstanceDownAlert

        total_second = days * 24 * 60 * 60
        start_date = timezone.now() - timezone.timedelta(days=days)

        alerts = InstanceDownAlert.objects.filter(service__in=self.services.filter(is_critical=True), severity=2, endsAt__gte=start_date) | InstanceDownAlert.objects.filter(service__in=self.services.filter(is_critical=True), severity=2, endsAt__isnull=True)

        total_unavailability = 0
        for alert in alerts:
            if alert.startsAt < start_date:
                total_unavailability += (alert.endsAt - start_date).seconds
            else:
                total_unavailability += alert.duration.seconds

        return round(100 - total_unavailability * 100 / total_second, 3)

    def __str__(self):
        return self.title

class Service(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete = models.CASCADE,
        related_name = "services",
    )
    title = models.CharField(max_length=128, blank=False)
    url = models.URLField(max_length=512, blank=False)
    is_public = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)
    is_critical = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")

    def availability(self, days=7):

        from alerts.models import InstanceDownAlert

        total_second = days * 24 * 60 * 60
        start_date = timezone.now() - timezone.timedelta(days=days)

        alerts = InstanceDownAlert.objects.filter(service=self, severity=2, endsAt__gte=start_date) | InstanceDownAlert.objects.filter(service=self, severity=2, endsAt__isnull=True)

        total_unavailability = 0
        for alert in alerts:
            if alert.startsAt < start_date:
                total_unavailability += (alert.endsAt - start_date).seconds
            else:
                total_unavailability += alert.duration.seconds

        return round(100 - total_unavailability * 100 / total_second, 3)

    def is_healthy(self):
        return not self.instancedownalerts.filter(endsAt__isnull=True)

    def is_critical_state(self):
        return self.instancedownalerts.filter(status=2, endsAt__isnull=True)

    def is_warning(self):
        return self.instancedownalerts.filter(status=2, endsAt__isnull=True)

    def __str__(self):
        return f'{self.application} - {self.title}'

class Metrics(models.Model):
    """
    Fetch {{url}}/metrics within prometheus
    Can be used for node_explorer or custom metrics
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "metrics",
    )
    url = models.URLField(max_length=512, blank=False)
    is_enabled = models.BooleanField(default=True)

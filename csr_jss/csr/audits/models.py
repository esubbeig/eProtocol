from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE)
    module = models.CharField(max_length=200)
    project = models.CharField(max_length=500, blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    previous_state = models.TextField(blank=True)
    current_state = models.TextField(blank=True)
    reason = models.CharField(max_length=2048, null=True)
    ip = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auditlog'

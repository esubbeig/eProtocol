from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser

class Roles(models.Model):
  USER_ROLE_CHOICES = (
      ('Global User', 'Global User'),
      ('CSR User', 'CSR User'),
      ('eProtocol User', 'eProtocol User'),
    )

  role   = models.CharField(max_length=100, choices=USER_ROLE_CHOICES, null=True, blank=True)


class User(AbstractUser):
    
    user_role   = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    phone       = models.CharField(max_length=10, null=True, blank=True)
    delete      = models.BooleanField(default=False)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


# to store encrypted user credentials
class CredInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key_pass = models.TextField(default=None, blank=True, null=True)
    updated_on   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'credinfo'
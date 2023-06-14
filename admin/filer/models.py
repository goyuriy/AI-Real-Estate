from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group

from accounts.models import Account


class Filer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)

    filename = models.CharField(max_length=255, null=False, default='', blank=True)
    url = models.FileField(null=False)
    mime = models.CharField(max_length=255, null=False, default='', blank=True)
    name = models.CharField(max_length=255, null=False, blank=True, default='')
    description = models.CharField(max_length=1500, null=False, blank=True, default='')

    created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)

    def __str__(self):
       return str(self.filename)

    class Meta:
        db_table = "filer_filers"
        verbose_name = _("Filer")
        verbose_name_plural = _("Filers")

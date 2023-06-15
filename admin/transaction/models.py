from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.forms.fields import MultipleChoiceField
from django.db.models.fields import CharField

from django.db import models
from django.utils.translation import gettext as _

# from markdownx.models import MarkdownxField
from easy_thumbnails import fields as e_fields

# from filer.models import Filer
from accounts.models import Account
from django import forms
# from utils import consts


status = [
    ('pending', 'Pending', ),
    ('in progress', 'In Progress', ),
    ('completed', 'Completed', ),
]

class Transaction(models.Model):
    name = models.CharField(max_length=150, null=False)

    status = models.CharField(max_length=50, choices=status, default='pending')

    address = models.CharField(max_length=150, default='')

    saller = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, related_name='saller')
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, related_name='buyer')

    started_at = models.DateTimeField(null=False, editable=True, default=datetime.now)
    created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    
    def __str__(self):
       return f"{self.name}, {str(self.pk)}"

    class Meta:
        db_table = "transaction_transactions"
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
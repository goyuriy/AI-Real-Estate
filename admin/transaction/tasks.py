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
from task.models import Task
from django import forms
# from utils import consts
from .models import TransactionTemplate

class TransactionTemplateTask(models.Model):
    template = models.ForeignKey(TransactionTemplate, on_delete=models.CASCADE, null=False, related_name='transaction_template')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, related_name='task')

    created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    
    def __str__(self):
       return f"{self.template.name}, {self.task.name}"

    class Meta:
        db_table = "transaction_template_tasks"
        verbose_name = _("template task")
        verbose_name_plural = _("template tasks")
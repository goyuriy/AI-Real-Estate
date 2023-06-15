from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.forms.fields import MultipleChoiceField
from django.db.models.fields import CharField

from django.db import models
from django.utils.translation import gettext as _

# from markdownx.models import MarkdownxField
from easy_thumbnails import fields as e_fields

from accounts.models import Account
from transaction.models import Transaction


task_priority = [
    ('low', 'Low', ),
    ('medium', 'Medium', ),
    ('high', 'High', ),
]

user_types = [
    ("fsbo-seller", "FSBO Seller", ),
    ( "buyer", "Buyer", ),
]

class UserTypesEnum(models.TextChoices):
    FSBO_SELLER = "fsbo-seller", "FSBO Seller"
    BUYER = "buyer", "Buyer"

status = [
    ('pending', 'Pending', ),
    ('in progress', 'In Progress', ),
    ('completed', 'Completed', ),
]


# Contribution by @cbows 
class _MultipleChoiceField(MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.pop("base_field", None)
        kwargs.pop("max_length", None)
        super().__init__(*args, **kwargs)


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": _MultipleChoiceField,
                                    "choices": self.base_field.choices,
                                    **kwargs})


class Task(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=False, default='')

    document_template = e_fields.ThumbnailerImageField(max_length=255, null=False, default='', blank=True,
        resize_source=dict(size=(140, 140), sharpen=True))
    
    assignee = ChoiceArrayField(CharField(max_length=24, choices=UserTypesEnum.choices), default=list)

    task_priority = models.CharField(max_length=50, choices=task_priority, default='low')
    is_listed = models.BooleanField(default=False)

    days_to_do = models.IntegerField(default=0, null=False)

    started_at = models.DateTimeField(null=False, blank=False, editable=False)
    created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    
    def __str__(self):
       return f"{self.name}, {str(self.pk)}"

    class Meta:
        db_table = "task_tasks"
        verbose_name = _("task")
        verbose_name_plural = _("tasks")


class AssignedTask(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False)

    status = models.CharField(max_length=50, choices=status, default='pending')

    # def save(self, *args, **kwargs):
    #     # if not self.founding_state and self.pk is None:
    #     #     self.founding_state = "AR"

    #     if 'fsbo-seller' in self.task.assignee:
    #         pass

    #     if 'buyer' in self.task.bu:
    #         pass

    #     print(self.task.assignee)
    #     print(self.transaction.saller.pk)

    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.task.name)}"

    class Meta:
        db_table = "task_assignees"
        verbose_name = _("Assigned Task")
        verbose_name_plural = _("Assigned Tasks")
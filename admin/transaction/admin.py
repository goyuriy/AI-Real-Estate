# from django import forms
# from django.conf import settings
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.forms.widgets import CheckboxSelectMultiple
# from django.utils.html import mark_safe

from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Transaction, TransactionTemplate
from .tasks import TransactionTemplateTask
from task.models import AssignedTask

class AssignedTaskInline(admin.TabularInline):
    model = AssignedTask
    readonly_fields = ('assignee_type', 'user', ) 
    can_delete = True
    extra=0


class TransactionTemplateTaskInline(admin.TabularInline):
    model = TransactionTemplateTask
    # readonly_fields = ('assignee_type', 'user', ) 
    can_delete = True
    extra=0


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["status", ]
    list_display = [
        "__str__", "name", 'status',
    ]

    inlines = [AssignedTaskInline]

    
@admin.register(TransactionTemplate)
class TransactionTemplateAdmin(admin.ModelAdmin):
    list_filter = ["county", "state", ]
    list_display = [
        "name", "county", 'state',
    ]

    inlines = [TransactionTemplateTaskInline]


@admin.register(TransactionTemplateTask)
class TransactionTemplateTaskAdmin(admin.ModelAdmin):
    list_display = [
        "id", "__str__",
    ]

    unique_together = ["template", "task"]
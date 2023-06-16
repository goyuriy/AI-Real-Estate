# from django import forms
# from django.conf import settings
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.forms.widgets import CheckboxSelectMultiple
# from django.utils.html import mark_safe

from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Transaction, TransactionTemplate
from .tasks import TransactionTemplateTask


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["status", ]
    list_display = [
        "__str__", "name", "address", 'status',
    ]

    
@admin.register(TransactionTemplate)
class TransactionTemplateAdmin(admin.ModelAdmin):
    list_filter = ["country", "state", ]
    list_display = [
        "name", "country", 'state',
    ]


@admin.register(TransactionTemplateTask)
class TransactionTemplateTaskAdmin(admin.ModelAdmin):
    list_display = [
        "id", "__str__",
    ]
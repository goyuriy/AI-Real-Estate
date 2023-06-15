# from django import forms
# from django.conf import settings
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.forms.widgets import CheckboxSelectMultiple
# from django.utils.html import mark_safe

from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Transaction #, OfferFiler


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["status", ]
    list_display = [
        "__str__", "name", "address", 'status',
    ]
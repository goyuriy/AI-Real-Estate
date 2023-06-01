from django import forms
from django.contrib import admin

from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ["identity_id", "created_at", "updated_at", "user_agent", "date_joined", "last_login"]
    pass

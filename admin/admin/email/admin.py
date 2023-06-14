import json

from django import forms
from django.contrib import admin
from django.db import connection
from django.forms import widgets
from django.forms.models import model_to_dict
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Email

SKIP_FIELDS = [
    "id",
]
meta_data_FIELDS = ["data", "meta_data", "log"]
OVERVIEW_FIELDS = [
    "recipient_email",
    "recipient_name",
    "sender_email",
    "sender_name",
    "subject",
    "template",
    "status",
    "created_at",
    "content_html",
    "sent_attemp_at",
]


class HtmlWidget(widgets.Widget):
    input_type = None

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ""
        return mark_safe("%s" % value)


class EmailAdminForm(forms.ModelForm):
    class Meta:
        model = Email
        widgets = {
            "content_html": HtmlWidget(),
        }
        fields = "__all__"


class EmailAdmin(admin.ModelAdmin):
    form = EmailAdminForm
    search_fields = (
        "recipient_email",
        "subject",
    )

    list_display = (
        "email_id",
        "recipient_email",
        "subject",
        "status",
        "created_at",
    )
    readonly_fields = ["content"]
    change_actions = [
        "resend",
    ]

    suit_form_tabs = (
        ("overview", "Overview"),
        ("event", "Event"),
        ("meta_data", "meta_data"),
    )

    fieldsets = [
        (
            None,
            {
                "classes": ("suit-tab suit-tab-overview",),
                "fields": OVERVIEW_FIELDS,
            },
        ),
        (
            None,
            {
                "classes": ("suit-tab suit-tab-meta_data",),
                "fields": meta_data_FIELDS,
            },
        ),
    ]

    def get_change_actions(self, request, object_id, form_url):
        if not self.has_change_permission(request, self.get_object(request, object_id)):
            return []

        return super().get_change_actions(request, object_id, form_url)

    def email_id(self, obj):
        return obj.id

    def content(self, obj):
        if obj:
            return mark_safe("%s" % obj.content_html)

        return ""

    def sent_canceled(self, obj):
        return obj.status

    sent_canceled.label = "Status"
    sent_canceled.short_description = "Status"

    list_filter = ("status", "template")

    def resend(self, request, obj, *args):

        data = model_to_dict(obj, exclude=["created_at", "sent_attemp_at", "content_html"])
        data["action"] = "send"
        buf = json.dumps(data)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT pg_notify('email_events', '{buf}');")

    resend.short_description = "Resend"
    resend.label = "Resend"
    resend.attrs = {
        "class": "btn btn-outline-primary buttonDisabled confirmation-farm",
        "objectaction_item": "list-item",
    }

admin.site.register(Email, EmailAdmin)

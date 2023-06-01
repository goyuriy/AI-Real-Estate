from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from utils import consts
from admin.utils import JSONField


class Email(models.Model):
    recipient_email = models.CharField(max_length=255, default="", blank=True)
    recipient_name = models.CharField(max_length=255, default="", blank=True)
    sender_email = models.CharField(max_length=255, default="info@webdevelop.pro", blank=True)
    sender_name = models.CharField(max_length=255, default="Pro Webdevelop Team", blank=True)
    subject = models.CharField(max_length=255, default="", blank=True)
    template = models.CharField(max_length=255, default="", choices=consts.email.EMAIL_TEMPLATES, blank=False)
    status = models.CharField(max_length=255, default="new", choices=[(k.value,k.value) for k in consts.email.StatusT], blank=False)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    data = JSONField(default=dict, blank=True)
    meta_data = JSONField(default=dict, blank=True)
    log = JSONField(default=dict, blank=True)
    content_html = models.TextField(
        default="",
        blank=True,
    )
    sent_attemp_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.recipient_email

    class Meta:
        db_table = "email_emails"
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")
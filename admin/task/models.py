from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

# from markdownx.models import MarkdownxField
from easy_thumbnails import fields as e_fields

# from filer.models import Filer
from accounts.models import Account
# from utils import consts


task_priority = [
    ('low', 'Low', ),
    ('medium', 'Medium', ),
    ('high', 'High', ),
]

status = [
    ('not listed', 'Not listed', ),
    ('pending', 'Pending', ),
    ('in progress', 'In Progress', ),
    ('completed', 'Completed', ),
]

# offer_filer_choices = [
#     ('company', 'Financial and investment documents', ),
#     ('tax', 'Tax documents', ),
#     ('investment-agreements', 'Investment-agreements',),
#     ('investor-updates', 'Investor updates', ),
#     ('other', 'Other', ),
# ]


# class OfferFiler(models.Model):
#     offer = models.ForeignKey('Offer', on_delete=models.CASCADE, null=False)
#     filer = models.ForeignKey(Filer, on_delete=models.CASCADE, null=False)
#     type = models.CharField(max_length=50, choices=offer_filer_choices)

#     def __str__(self):
#        return f"{self.type}, {str(self.filer.filename)}"

#     class Meta:
#         db_table = "offer_offer_filers"
#         verbose_name = _("offer filer")
#         verbose_name_plural = _("offer filers")


class Task(models.Model):
    # user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)

    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=False, default='')

    document_template = e_fields.ThumbnailerImageField(max_length=255, null=False, default='', blank=True,
        resize_source=dict(size=(140, 140), sharpen=True))

    task_priority = models.CharField(max_length=50, choices=task_priority, default='low')
    status = models.CharField(max_length=50, choices=status, default='not listed')

    days_to_do = models.IntegerField(default=0, null=False)

    started_at = models.DateTimeField(null=False, blank=False, editable=False)
    created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    

    # slug = models.CharField(max_length=150, null=False, unique=True)
    # min_investment = models.DecimalField(max_digits=12, decimal_places=2, null=False)

    
    # title = models.CharField(max_length=255, null=False, default='')
    # highlights = models.TextField(null=False, default='')
    # image = e_fields.ThumbnailerImageField(max_length=255, null=False, default='', blank=True,
    #     resize_source=dict(size=(140, 140), sharpen=True))
    # # filers = models.ManyToManyField(Filer, through=OfferFiler)

    # valuation = models.DecimalField(max_digits=14, decimal_places=2, default=0.0, null=False)
    # total_shares = models.IntegerField(default=0, null=False)
    # price_per_share = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, null=False)
    # status = models.CharField(max_length=255, null=False, default='new', choices=[(k.value,k.value) for k in consts.offer.StatusT])
    # security_type = models.CharField(max_length=255, null=False, choices=[(k.value,k.value) for k in consts.offer.SecurityT])
    # notes = models.TextField(null=False, default='', blank=True)
    # subscribed_shares = models.IntegerField(default=0, null=False)
    # confirmed_shares = models.IntegerField(default=0, null=False)
    # additional_details = models.TextField(null=False, default='', blank=True)
    # website = models.CharField(max_length=255, null=False, default='', blank=True)
    # country = models.CharField(max_length=25, null=False, default='USA', blank=True)
    # state = models.CharField(max_length=50, null=False, default='', blank=True)
    # city = models.CharField(max_length=50, null=False, default='', blank=True)
    # zip_code = models.CharField(max_length=25, null=False, default='', blank=True, help_text='Company Index')
    # address1 = models.CharField(max_length=150, null=False, default='', blank=True, help_text='Company address')
    # address2 = models.CharField(max_length=150, null=False, default='', blank=True, help_text='Additional address information')
    # seo_title = models.CharField(max_length=255, null=False, default='', blank=True)
    # seo_description = models.CharField(max_length=255, null=False, default='', blank=True)

    # closing_at = models.DateTimeField(null=False, blank=False)
    # created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    # updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)

    def __str__(self):
       return f"{self.name}, {str(self.pk)}"

    class Meta:
        db_table = "task_tasks"
        verbose_name = _("task")
        verbose_name_plural = _("tasks")


class AssignedTask(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False)

    completed = models.BooleanField(default=False)

    def __str__(self):
       return str(self.pk)

    class Meta:
        db_table = "task_assignees"
        verbose_name = _("Assigned Task")
        verbose_name_plural = _("Assigned Tasks")
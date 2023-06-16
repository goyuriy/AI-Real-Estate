from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

# from filer.models import Filer
from accounts.models import Account


status = [
    ('pending', 'Pending', ),
    ('in progress', 'In Progress', ),
    ('completed', 'Completed', ),
]

countries = [
    ('USA', 'USA' ),
]

states = [
    ('AL', 'AL (Alabama)' ),
    ('AK', 'AK (Alaska)' ),
    ('AZ', 'AZ (Arizona)' ),
    ('AR', 'AR (Arkansas)' ),
    ('CA', 'CA (California)' ),
    ('CO', 'CO (Colorado)' ),
    ('CT', 'CT (Connecticut)' ),
    ('DE', 'DE (Delaware)' ),
    ('FL', 'FL (Florida)' ),
    ('GA', 'GA (Georgia)' ),
    ('HI', 'HI (Hawaii)' ),
    ('ID', 'ID (Idaho)' ),
    ('IL', 'IL (Illinois)' ),
    ('IN', 'IN (Indiana)' ),
    ('IA', 'IA (Iowa)' ),
    ('KS', 'KS (Kansas)' ),
    ('KY', 'KY (Kentucky)' ),
    ('LA', 'LA (Louisiana)' ),
    ('ME', 'ME (Maine)' ),
    ('MD', 'MD (Maryland)' ),
    ('MA', 'MA (Massachusetts)' ),
    ('MI', 'MI (Michigan)' ),
    ('MN', 'MN (Minnesota)' ),
    ('MS', 'MS (Mississippi)' ),
    ('MO', 'MO (Missouri)' ),
    ('MT', 'MT (Montana)' ),
    ('NE', 'NE (Nebraska)' ),
    ('NV', 'NV (Nevada)' ),
    ('NH', 'NH (New) Hampshire' ),
    ('NJ', 'NJ (New) Jersey' ),
    ('NM', 'NM (New) Mexico' ),
    ('NY', 'NY (New) York' ),
    ('NC', 'NC (North) Carolina' ),
    ('ND', 'ND (North) Dakota' ),
    ('OH', 'OH (Ohio)' ),
    ('OK', 'OK (Oklahoma)' ),
    ('OR', 'OR (Oregon)' ),
    ('PA', 'PA (Pennsylvania)' ),
    ('RI', 'RI (Rhode) Island' ),
    ('SC', 'SC (South) Carolina' ),
    ('SD', 'SD (South) Dakota' ),
    ('TN', 'TN (Tennessee)' ),
    ('TX', 'TX (Texas)' ),
    ('UT', 'UT (Utah)' ),
    ('VT', 'VT (Vermont)' ),
    ('VA', 'VA (Virginia)' ),
    ('WA', 'WA (Washington)' ),
    ('WV', 'WV (West) Virginia' ),
    ('WI', 'WI (Wisconsin)' ),
    ('WY', 'WY (Wyoming)', ),
]


class TransactionTemplate(models.Model):
    name = models.CharField(max_length=150, null=False)

    state = models.CharField(max_length=50, choices=states)
    country = models.CharField(max_length=50, choices=countries)

    created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    
    def __str__(self):
       return f"{self.name}"

    class Meta:
        db_table = "transaction_template"
        verbose_name = _("transaction template")
        verbose_name_plural = _("transaction templates")


class Transaction(models.Model):
    name = models.CharField(max_length=150, null=False)

    status = models.CharField(max_length=50, choices=status, default='pending')

    address = models.CharField(max_length=150, default='')

    saller = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, related_name='saller')
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, related_name='buyer')

    template = models.ForeignKey(TransactionTemplate, on_delete=models.CASCADE, blank=True, null=True, related_name='template')

    started_at = models.DateTimeField(null=False, editable=True, default=datetime.now)
    created_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    updated_at = models.DateTimeField(null=False, editable=False, default=datetime.now)
    
    def __str__(self):
       return f"{self.name}"

    class Meta:
        db_table = "transaction_transactions"
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
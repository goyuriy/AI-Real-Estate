import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from easy_thumbnails.fields import ThumbnailerImageField

from .managers import AccountManager
from admin.utils import JSONField


class Account(AbstractBaseUser, PermissionsMixin):

    # id = models.IntegerField(primary_key=True, editable=False, null=False)
    password = models.CharField(_("password"), max_length=128, editable=False)
    identity_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={"unique": _("That email already used")},
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    image = ThumbnailerImageField(
        upload_to="avatar",
        blank=True,
        null=False,
        # resize_source=settings.CUSTOM_AVATAR_THUMBNAIL_OPTIONS,
        # storage=public_storage,
    )
    # ToDo rename to create_at, updated_at
    date_joined = models.DateTimeField(
        _("date joined"), blank=True, null=False, default=datetime.now
    )
    last_login = models.DateTimeField(
        _("last login"), blank=True, null=False, default=datetime.min
    )


    social = models.CharField(
        verbose_name="Registration via", max_length=20, default="", blank=True
    )
    linkedin_id = models.CharField(max_length=20, editable=False)
    facebook_id = models.CharField(max_length=20, editable=False)
    google_id = models.CharField(max_length=30, editable=False)
    ip_address = models.GenericIPAddressField(default="0.0.0.0", editable=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    data = JSONField(default=dict, null=False, blank=True)
    user_agent = models.CharField(max_length=1024, editable=False, default='', null=False)
    # auth_provider = models.CharField(max_length=108, choices=XXX)
    social = models.CharField(max_length=20, default='', null=False)
    # timezone = models.CharField(max_length=64, default='', null=False)

    created_at = models.DateTimeField(blank=True, default=timezone.now, editable=False)
    updated_at = models.DateTimeField(blank=True, default=timezone.now, editable=False)

    objects = AccountManager()

    class Meta:
        db_table = "user_users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    USERNAME_FIELD = "email"

    @property
    def is_only_staff(self):
        return self.is_active and not self.is_superuser and self.is_staff

    def has_perm(self, perm, obj=None):
        if self.is_only_staff and "view" in perm:
            return True

        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_only_staff:
            return True

        return super().has_module_perms(app_label)

    @property
    def full_name(self):
        if not self.first_name and not self.last_name:
            return self.id
        return f"{self.first_name} {self.last_name}"

    def __str__(self):  # __unicode__ on Python 2
        return self.email

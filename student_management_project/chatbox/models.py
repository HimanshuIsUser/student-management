from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    last_login = models.DateTimeField(blank=True, null=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class StudentDetails(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_user = models.ForeignKey('CustomUser', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    no_of_update = models.IntegerField(blank=True, null=True)
    updated_at_date = models.DateField(default = timezone.now)
    class Meta:
        managed = True
        db_table = 'tbl_student_details'
import datetime
from email.policy import default
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User

from services.models import Ayadat


# Create your models here.

class TimeStampMixin(models.Model):
    is_deleted      = models.BooleanField (default=False)
    created_at      = models.DateTimeField(auto_now_add=True,null=True)
    created_at_date = models.DateField(auto_now_add=True,null=True)
    updated_at      = models.DateTimeField(auto_now=True,null=True)
    updated_at_date = models.DateField(auto_now=True,null=True)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, 'name'):
            if self.name != None:
                return str(self.name)
            else:
                return str("object")
        else:
                return str("object")

# Create your models here.
class specific(TimeStampMixin,models.Model):
    name  = models.CharField(max_length=100,default='-', verbose_name="اسم التخصص")

class Category(TimeStampMixin,models.Model):
    specific  = models.ForeignKey('specific', on_delete=models.CASCADE, verbose_name="التخصص")
    ayada = models.ForeignKey('services.Ayadat', related_name='category_ayada', on_delete=models.CASCADE, verbose_name="العيادة")

    def __str__(self):
        return self.specific.name

class DailyReport(TimeStampMixin,models.Model):
    day      = models.DateField(auto_now_add=True,null=True, verbose_name="تاريخ اليوم")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="تخصص العيادة")
    ayada    =models.ForeignKey('services.Ayadat', on_delete=models.CASCADE, verbose_name="العيادة",null=True)
    num      = models.IntegerField(verbose_name="عدد المترددين")

    def __str__(self):
        return self.category
import datetime
from email.policy import default
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.db import models
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



class Area(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100,default='-')

class Law(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100,default='-')

class Ayadat(TimeStampMixin, models.Model):
    name = models.CharField(max_length=50, default="تجربة")
    area = models.ForeignKey('Area', related_name='ayada_area', on_delete=models.CASCADE)

class Entity(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100, default='-')


# another name for services
class Service(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100, default='-', verbose_name='اسم الخدمة')

class Letter(TimeStampMixin,models.Model):
    # first part  patient info
    name        = models.CharField(max_length=50, default="تجربة")
    naId        = models.CharField(max_length=14, default="2980504252201")
    by_doctor   = models.CharField(max_length=50, default="-") # doctor
    law         = models.ForeignKey('Law', related_name='letter_law', on_delete=models.CASCADE)
    ayada       = models.ForeignKey('Ayadat', related_name='letter_law', on_delete=models.CASCADE)
    diagnosis   = models.CharField(max_length=50, default="-", verbose_name="التشخيص") # التشخيص
    description = models.CharField(max_length=50, default="-", verbose_name="وصف الحالة")
    
    # second part  services info
    price       = models.IntegerField(default=0, verbose_name="الرسوم المقررة")
    services    = models.ManyToManyField('Service', blank=True, null=True, related_name='letters',verbose_name="الخدمات")
    entity      = models.ForeignKey('Entity', related_name='letter_entity', on_delete=models.CASCADE)
    created_by  = models.CharField(max_length=50, default="-", blank=True, null=True) # created by employee 


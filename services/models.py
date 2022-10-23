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
    name        = models.CharField(max_length=50, verbose_name="اسم المريض ثلاثى")
    naId        = models.CharField(max_length=14, verbose_name="الرقم القومى")
    by_doctor   = models.CharField(max_length=50, verbose_name="مقرر الإجراء") # doctor
    law         = models.ForeignKey('Law', related_name='letter_law', on_delete=models.CASCADE, verbose_name="قانون الانتفاع")
    ayada       = models.ForeignKey('Ayadat', related_name='letter_law', on_delete=models.CASCADE, verbose_name="العيادة المحول منها")
    diagnosis   = models.CharField(max_length=50, default="-", verbose_name="التشخيص") # التشخيص
    description = models.CharField(max_length=50, default="-", verbose_name="وصف الحالة")
    
    # second part  services info
    price       = models.IntegerField(default=0, verbose_name="الرسوم المقررة")
    services    = models.ManyToManyField('Service', blank=True, related_name='services',verbose_name="الخدمات")
    entity      = models.ForeignKey('Entity', related_name='letter_entity', on_delete=models.CASCADE, verbose_name="الجهة")
    created_by  = models.CharField(max_length=50, default="-", verbose_name="مسئول التسجيل") # created by employee 


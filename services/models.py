import datetime
from email.policy import default
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User


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
    # is ayada make customer letters or not
    is_letter = models.BooleanField(default=True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area =  models.ForeignKey('Ayadat', related_name='employee_ayada', on_delete=models.CASCADE, null=True, blank=True)
    area2 = models.ManyToManyField('Ayadat',related_name='employee_ayadat')

class EntityMainClass(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100, default='-', verbose_name='التصنيف الرئيسى', db_index=True)

class EntitySubClass(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100, default='-', verbose_name='التصنيف الرئيسى', db_index=True)

class Entity(TimeStampMixin,models.Model):
    name    = models.CharField(max_length=100, default='-', db_index=True)
    phone   = models.CharField(max_length=20, default='-')
    address = models.CharField(max_length=100, default='-')
    mainClass = models.ForeignKey('EntityMainClass', related_name='entity_main', default=3, on_delete=models.CASCADE, verbose_name="التصنيف الرئيسى",null=True, db_index=True)
    subClass  = models.ForeignKey('EntitySubClass', related_name='entity_sub', default=5, on_delete=models.CASCADE, verbose_name="التصنيف الفرعى",null=True, db_index=True)

# ===

class ServiceMainClass(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100, default='-', verbose_name='التصنيف الرئيسى', db_index=True)

class ServiceSubClass(TimeStampMixin,models.Model):
    name = models.CharField(max_length=100, default='-', verbose_name='التصنيف الفرعى', db_index=True)


class Service(TimeStampMixin,models.Model):
    name      = models.CharField(max_length=250, default='-', verbose_name='اسم الخدمة', db_index=True)
    mainClass = models.ForeignKey('ServiceMainClass', related_name='service_main', on_delete=models.CASCADE, verbose_name="التصنيف الرئيسى",null=True, db_index=True)
    subClass  = models.ForeignKey('ServiceSubClass', related_name='service_sub', on_delete=models.CASCADE, verbose_name="التصنيف الفرعى",null=True, db_index=True)
    code      = models.IntegerField(unique=True,null=True, db_index=True)
    price     = models.IntegerField(unique=True,null=True, blank=True)

class EntityService(TimeStampMixin,models.Model):
    entity   = models.ForeignKey('Entity', related_name='entity_service', on_delete=models.CASCADE, verbose_name="الجهة",null=True, db_index=True)
    services = models.ManyToManyField('Service',related_name='services_entity', default='-')

class Letter(TimeStampMixin,models.Model):
    # first part  patient info
    serial      = models.IntegerField(db_index=True, unique=True, null=True)
    name        = models.CharField(max_length=50, verbose_name="اسم المريض ثلاثى", db_index=True)
    naId        = models.CharField(max_length=14, verbose_name="الرقم القومى", db_index=True)
    by_doctor   = models.CharField(max_length=50, verbose_name="مقرر الإجراء") # doctor
    law         = models.ForeignKey('Law', related_name='letter_law', on_delete=models.CASCADE, verbose_name="قانون الانتفاع")
    ayada       = models.ForeignKey('Ayadat', related_name='letter_law', on_delete=models.CASCADE, verbose_name="العيادة المحول منها")
    diagnosis   = models.CharField(max_length=50, default=" ", verbose_name="التشخيص") # التشخيص
    description = models.TextField(max_length=250, default=" ", verbose_name="وصف الحالة")
    # second part  services info
    price       = models.IntegerField(default=0, verbose_name="الرسوم المقررة")
    services    = models.ManyToManyField('Service', blank=True, related_name='services',verbose_name="الخدمات")
    entity      = models.ForeignKey('Entity', related_name='letter_entity', on_delete=models.CASCADE, verbose_name="الجهة")
    created_by  = models.CharField(max_length=50, default="-", verbose_name="مسئول التسجيل") # created by employee
    notes       = models.CharField(max_length=50, default="", null=True, blank=True)
    cancelReason= models.CharField(max_length=50, default="", null=True, blank=True)


class ServicePrice(TimeStampMixin,models.Model):
    name  = models.ForeignKey('Service', related_name='service_price', on_delete=models.CASCADE, verbose_name="اسم الخدمة")
    publicPrice = models.IntegerField(default=0, verbose_name="توريد المنتفع")
    price = models.IntegerField(default=0, verbose_name="الرسوم المقررة")
    notes = models.CharField(max_length=50, default=" ", verbose_name="ملاحظات")
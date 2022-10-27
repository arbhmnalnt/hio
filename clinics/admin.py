from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.


class SpecificAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['ayada__name']
    list_display = ('specific','ayada','created_at_date')

class DailyReportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['day', 'ayada__name']
    list_display = ('day','category','ayada','num')

admin.site.register(specific, SpecificAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(DailyReport, DailyReportAdmin)
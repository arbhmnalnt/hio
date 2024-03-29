from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin , ExportActionMixin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

class DailyReportHistoryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('day', 'user', 'created_at')

class SpecificAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['ayada__name']
    list_display = ('specific','ayada','created_at_date')

class DailyReportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['id', 'day', 'ayada__name']
    list_display = ('day','category','ayada','specialist','advisory','papers', 'childPapers','num')

admin.site.register(DailyReportHistory, DailyReportHistoryAdmin)
admin.site.register(specific, SpecificAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(DailyReport, DailyReportAdmin)
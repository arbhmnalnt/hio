from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
#  optimizing the query for each service
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.prefetch_related('services')

#     def get_services(self, obj):
#         return " - ".join([service.name for service in obj.services.all()])

class LetterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name','naId', 'entity','created_at_date', 'created_by')

class ServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class EntityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class AyadatAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'area')

class LawAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class AreaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Area, AreaAdmin)
admin.site.register(Law, LawAdmin)
admin.site.register(Ayadat, AyadatAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Letter, LetterAdmin)

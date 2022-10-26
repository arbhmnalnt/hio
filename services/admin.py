from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'موظف'

class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]

class LetterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name','naId','get_services', 'entity','created_at_date', 'created_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('services')

    def get_services(self, obj):
        return " - ".join([service.name for service in obj.services.all()])

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

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Area, AreaAdmin)
admin.site.register(Law, LawAdmin)
admin.site.register(Ayadat, AyadatAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Letter, LetterAdmin)

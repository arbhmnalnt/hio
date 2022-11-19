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

class ServiceSubClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class ServiceMainClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class EntityMainClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class EntitySubClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class LetterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['serial','name', 'naId']
    list_display = ('name','naId','get_services', 'entity','created_at_date', 'created_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('services')

    def get_services(self, obj):
        return " - ".join([service.name for service in obj.services.all()])

class ServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'get_mainClass_name', 'get_subClass_name', 'code', 'price')
    search_fields = ['name', 'mainClass__name', 'subClass__name']


    def get_mainClass_name(self, obj):
        return obj.mainClass.name
    get_mainClass_name.admin_order_field  = 'name'  #Allows column order sorting
    get_mainClass_name.short_description = 'التصنيف الرئيسى'  #Renames column he

    def get_subClass_name(self, obj):
        return obj.subClass.name
    get_subClass_name.admin_order_field  = 'name'  #Allows column order sorting
    get_subClass_name.short_description = 'التصنيف الفرعى'  #Renames column he

class EntityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'get_mainClass_name', 'get_subClass_name', 'address', 'phone')

    def get_mainClass_name(self, obj):
        return obj.mainClass.name
    get_mainClass_name.admin_order_field  = 'name'  #Allows column order sorting
    get_mainClass_name.short_description = 'التصنيف الرئيسى'  #Renames column he

    def get_subClass_name(self, obj):
        return obj.subClass.name
    get_subClass_name.admin_order_field  = 'name'  #Allows column order sorting
    get_subClass_name.short_description = 'التصنيف الفرعى'  #Renames column he

class AyadatAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'area')

class LawAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class AreaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class ServiceSubClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)

class EntityServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('get_entity_name', 'get_services')

    def get_entity_name(self, obj):
        return obj.entity.name

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('services_entity')

    def get_services(self, obj):
        return " - ".join([service.name for service in obj.services.all()])

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(EntityMainClass  ,EntityMainClassAdmin)
admin.site.register(EntitySubClass   ,EntitySubClassAdmin)
admin.site.register(ServiceMainClass ,ServiceMainClassAdmin)
admin.site.register(ServiceSubClass  ,ServiceSubClassAdmin)
admin.site.register(EntityService    ,EntityServiceAdmin)

admin.site.register(Area, AreaAdmin)
admin.site.register(Law, LawAdmin)
admin.site.register(Ayadat, AyadatAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Letter, LetterAdmin)

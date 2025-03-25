from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import (
    Collaborator, Task, Article, Purchase, PurchaseDetail, 
    ToolMaintenance, WorkingDay, WorkingDayResource, SaleProduct,
    CustomUser
)
from django.utils.html import format_html

admin.site.unregister(Group)

## PRUEBAS
class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1  # Número de filas vacías que se mostrarán para agregar nuevos detalles
    verbose_name = "Articulo"
    
class WorkingDayResourceInline(admin.TabularInline):
    model = WorkingDayResource
    extra = 1 
    verbose_name = "Recurso"
    
@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'phone')
    search_fields = ('firstname', 'lastname')
    list_filter = ('lastname',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'pay_per_day')
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'um', 'stock', 'type')
    search_fields = ('name',)
    list_filter = ('type',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('provider', 'date', 'get_details_names')
    search_fields = ('provider',)
    list_filter = ('date',)
    inlines = [PurchaseDetailInline]
    
    @admin.display(description='Detalles')
    def get_details_names(self, obj):
        details = obj.details.all()
        return format_html("<br>".join([detail.article.name for detail in details]))

# @admin.register(PurchaseDetail)
# class PurchaseDetailAdmin(admin.ModelAdmin):
#     list_display = ('purchase', 'article', 'unit_cost', 'units')
#     search_fields = ('article__name', 'purchase__provider')

@admin.register(ToolMaintenance)
class ToolMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('article', 'provider', 'cost', 'date')
    search_fields = ('article__name', 'provider')

@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ('collaborator', 'task', 'date', 'pay', 'paid', 'balance', 'is_done', 'is_canceled')
    search_fields = ('collaborator__firstname', 'collaborator__lastname', 'task__name')
    list_filter = ('date', 'is_done', 'is_canceled')
    inlines = [WorkingDayResourceInline]

# @admin.register(WorkingDayResource)
# class WorkingDayResourceAdmin(admin.ModelAdmin):
#     list_display = ('working_day', 'article', 'units')
#     search_fields = ('working_day__collaborator__firstname', 'working_day__task__name', 'article__name')

@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('client', 'kilos', 'price_kilo', 'total', 'discount')
    search_fields = ('client',)
    
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'avatar')
    search_fields = ('username', 'email', 'first_name', 'last_name')
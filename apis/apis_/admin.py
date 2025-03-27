from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import (
    Collaborator, Task, Article, Purchase, PurchaseDetail, 
    ToolMaintenance, WorkingDay, WorkingDayResource, SaleProduct,
    CustomUser, Customer, Workshop, Provider, Kpi
)
from django.utils.html import format_html
from django.db import models
from django.db.models import Sum
from django.urls import reverse
import locale
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from decimal import Decimal

# CONFIGS
locale.setlocale(locale.LC_TIME, 'es_ES.utf8') # Asegurar que los nombres de días estén en español linux
locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252') # Asegurar que los nombres de días estén en español windows
admin.site.unregister(Group)

# FORMS
class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = '__all__'
        
    class Media:
        js = ('admin/js/saleproduct.js',) 
            
    def clean_charged(self):
        charged = self.cleaned_data.get("charged")
        total = self.cleaned_data.get("total")

        if charged and total and charged > total:
            raise ValidationError("El monto cobrado no puede ser mayor que el total.")

        return charged
    
## SUBLISTAS
class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1  # Número de filas vacías
    verbose_name = "Articulo"
    
class WorkingDayResourceInline(admin.TabularInline):
    model = WorkingDayResource
    extra = 1 
    verbose_name = "Recurso"
    
# PAGES
@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'phone')
    search_fields = ('firstname', 'lastname', 'address')
    list_filter = ('firstname','lastname','address')
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city')
    search_fields = ('name', 'city')
    list_filter = ('name', 'city')
    
@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city')
    search_fields = ('name', 'city')
    list_filter = ('name', 'city')

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city')
    search_fields = ('name', 'city')
    list_filter = ('name', 'city')

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
    list_display = ('provider', 'date_format', 'get_details_names', 'delete_link')
    search_fields = ('provider__name',)
    list_filter = ('provider','date',)
    # readonly_fields= ("total",)
    inlines = [PurchaseDetailInline]
    list_per_page = 20
    ordering = ['-date']  
    actions = None 
    
    @admin.display(description='Articulos')
    def get_details_names(self, obj):
        details = obj.details.all()
        return format_html("<hr>".join([detail.article.name for detail in details]))

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data'):
            cl = self.get_changelist_instance(request)  # Obtiene la lista filtrada
            queryset = cl.get_queryset(request)  # Aplica los filtros activos

            # calcular balance
            total_balance_ = sum(
                (item.total or 0) - (item.paid or 0) 
                for item in queryset
            )
            
            total_payneto = sum(item.total or 0 for item in queryset)
            total_paid = sum(item.paid or 0 for item in queryset) 
            total_balance = "{:,.2f}".format(total_balance_).replace(",", "X").replace(".", ",").replace("X", ".") 

            extra_context = extra_context or {}
            extra_context['total_payneto'] = total_payneto
            extra_context['total_paid'] = total_paid
            extra_context['total_balance'] = total_balance
            response.context_data.update(extra_context)

        return response
    
    @admin.display(description='Fecha')
    def date_format(self, obj):
        return obj.date.strftime('%A %d/%m/%Y').capitalize()
    date_format.admin_order_field = 'date'
    
    def delete_link(self, obj):
        return format_html(
            '<a href="{}" style="color: red;" onclick="return true")"><i class="fa-solid fa-trash" /></a>',
            reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        )

    delete_link.short_description = 'Eliminar'

@admin.register(PurchaseDetail)
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'article', 'unit_cost', 'units')
    search_fields = ('article__name', 'purchase__provider')

@admin.register(ToolMaintenance)
class ToolMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('workshop', 'article', 'desc','date_format', 'cost', 'paid', 'balance', 'is_paid','delete_link')
    search_fields = ('workshop__name', 'article__name')
    list_filter = ('workshop', 'article', 'is_paid')
    list_per_page = 20
    ordering = ['-date']  
    actions = None 
    
    @admin.display(description='Fecha')
    def date_format(self, obj):
        return obj.date.strftime('%A %d/%m/%Y').capitalize()
    date_format.admin_order_field = 'date'
    
    @admin.display(description='Saldo')
    def balance(self, obj):
        cost = obj.cost or 0
        paid = obj.paid or 0
        balance = cost - paid
        return "{:,.2f}".format(balance).replace(",", "X").replace(".", ",").replace("X", ".")

    def delete_link(self, obj):
        return format_html(
            '<a href="{}" style="color: red;" onclick="return true")"><i class="fa-solid fa-trash" /></a>',
            reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        )

    delete_link.short_description = 'Eliminar'

@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ('collaborator', 'task', 'date_format', 'paid_neto' ,'paid', 'balance', 'get_resource_names', 'is_done', 'is_canceled', 'delete_link')
    search_fields = ('collaborator__firstname', 'collaborator__lastname', 'task__name')
    list_filter = ('collaborator__firstname', 'date', 'is_done', 'is_canceled')
    inlines = [WorkingDayResourceInline]
    list_per_page = 20
    ordering = ['-date']  
    actions = None 
    
    @admin.display(description='Fecha')
    def date_format(self, obj):
        return obj.date.strftime('%A %d/%m/%Y').capitalize()
    date_format.admin_order_field = 'date'
    
    @admin.display(description='Pagar')
    def paid_neto(self, obj):
        tariff = obj.tariff or 0
        discount = obj.discount or 0
        total = tariff - discount
        return "{:,.2f}".format(total).replace(",", "X").replace(".", ",").replace("X", ".")
    
    @admin.display(description='Saldo')
    def balance(self, obj):
        tariff = obj.tariff or 0
        discount = obj.discount or 0
        paid = obj.paid or 0
        balance = tariff - discount - paid
        return "{:,.2f}".format(balance).replace(",", "X").replace(".", ",").replace("X", ".")
    
    @admin.display(description='Recursos')
    def get_resource_names(self, obj):
        resources = obj.resources.all()
        return format_html("<hr>".join([f"{resource.article.name} {resource.units} {resource.article.um}" for resource in resources]))

    def changelist_view(self, request, extra_context=None):
            response = super().changelist_view(request, extra_context=extra_context)

            if hasattr(response, 'context_data'):
                cl = self.get_changelist_instance(request)  # Obtiene la lista filtrada
                queryset = cl.get_queryset(request)  # Aplica los filtros activos

                # calcular total pago neto
                total_payneto_ = sum(
                    (item.tariff or 0) - (item.discount or 0) 
                    for item in queryset
                )
                total_balance_ = sum(
                    (item.tariff or 0) - (item.discount or 0)  - (item.paid or 0) 
                    for item in queryset
                )
                
                total_payneto = "{:,.2f}".format(total_payneto_).replace(",", "X").replace(".", ",").replace("X", ".")
                total_paid = sum(item.paid or 0 for item in queryset) 
                total_balance = "{:,.2f}".format(total_balance_).replace(",", "X").replace(".", ",").replace("X", ".")

                extra_context = extra_context or {}
                extra_context['total_payneto'] = total_payneto
                extra_context['total_paid'] = total_paid
                extra_context['total_balance'] = total_balance
                response.context_data.update(extra_context)

            return response

    def delete_link(self, obj):
        return format_html(
            '<a href="{}" style="color: red;" onclick="return true")"><i class="fa-solid fa-trash" /></a>',
            reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        )

    delete_link.short_description = 'Eliminar'  # Nombre de la columna
            
@admin.register(WorkingDayResource)
class WorkingDayResourceAdmin(admin.ModelAdmin):
    list_display = ('working_day', 'article', 'units')
    search_fields = ('working_day__collaborator__firstname', 'working_day__task__name', 'article__name')

@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    form = SaleProductForm
    fields = ["date", "client", "kilos", "price_kilo", "discount", "discount_reazon","total", "is_paid", "charged"]
    list_display = ('client', 'date_format','kilos', 'price_kilo', 'discount', 'total', 'charged', 'receivable', 'is_paid','delete_link')
    search_fields = ('client__name', )
    list_filter = ('client', 'date', 'is_paid')
    list_per_page = 20
    ordering = ['-date']  
    actions = None
    
    class Media:
        css = {
            "all": ("admin/css/styles.css",)
        }
    
    @admin.display(description='Fecha')
    def date_format(self, obj):
        return obj.date.strftime('%A %d/%m/%Y').capitalize()
    date_format.admin_order_field = 'date'
    
    @admin.display(description='Por Cobrar S/')
    def receivable(self, obj):
        total = obj.total or 0
        charged = obj.charged or 0
        receivable = total - charged
        return "{:,.2f}".format(receivable).replace(",", "X").replace(".", ",").replace("X", ".")
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data'):
            cl = self.get_changelist_instance(request)  # Obtiene la lista filtrada
            queryset = cl.get_queryset(request)  # Aplica los filtros activos

            total_total_ = sum(
                (item.kilos or 0) * (item.price_kilo or 0) 
                for item in queryset
            )
            
            total_balance_ = sum(
                (item.total or 0) - (item.charged or 0) 
                for item in queryset
            )
            
            total_total = "{:,.2f}".format(total_total_).replace(",", "X").replace(".", ",").replace("X", ".")
            total_discount = sum(item.discount or 0 for item in queryset)
            total_payneto = sum(item.total or 0 for item in queryset)
            total_paid = sum(item.charged or 0 for item in queryset) 
            total_balance = "{:,.2f}".format(total_balance_).replace(",", "X").replace(".", ",").replace("X", ".")
            

            extra_context = extra_context or {}
            extra_context['total_total'] = total_total
            extra_context['total_discount'] = total_discount
            extra_context['total_payneto'] = total_payneto
            extra_context['total_paid'] = total_paid
            extra_context['total_balance'] = total_balance
            response.context_data.update(extra_context)

        return response

    def delete_link(self, obj):
        return format_html(
            '<a href="{}" style="color: red;" onclick="return true")"><i class="fa-solid fa-trash" /></a>',
            reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        )

    delete_link.short_description = 'Eliminar'
    
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'avatar')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
@admin.register(Kpi)
class KpiAdmin(admin.ModelAdmin):
    def dashboard_iframe(self, obj=None):
        return mark_safe('<iframe src="/dash/app/dashb" width="100%" height="600px" style="border:none;"></iframe>')

    dashboard_iframe.short_description = "Dashboard"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["dashboard_iframe"] = self.dashboard_iframe()
        return super().changelist_view(request, extra_context=extra_context)
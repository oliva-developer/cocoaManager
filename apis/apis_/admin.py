from django import forms
from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib.auth.models import User, Group
from .models import (
    Collaborator, Task, Article, Purchase, PurchaseDetail, 
    ToolMaintenance, WorkingDay,SaleProduct,
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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import platform

# Detectar el sistema operativo
sistema_operativo = platform.system()

# Configurar locale según el sistema operativo
if sistema_operativo == "Linux":
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    locale.setlocale(locale.LC_MONETARY, 'es_PE.utf8')
elif sistema_operativo == "Windows":
    locale.setlocale(locale.LC_TIME, 'Spanish')
    locale.setlocale(locale.LC_NUMERIC, 'English_United States.1252')
    locale.setlocale(locale.LC_MONETARY, 'Spanish_Peru.1252')
else:
    print("Sistema operativo no reconocido, no se aplicó locale.")

# ACTIONS
from collections import defaultdict

# ACTIONS
def exp_pdf_workingday(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    # Obtener la fecha actual en formato d-m-año
    fecha_actual = datetime.now().strftime("%d-%m-%Y")

    # Asignar el nombre del archivo con la fecha actual
    response['Content-Disposition'] = f'attachment; filename="jornadas_{fecha_actual}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    titulo = f"Lista de Jornadas Laborales - Hasta {fecha_actual}"

    pdf.setFont("Helvetica-Bold", 14)

    # Posición del texto
    x_titulo = width / 2
    y_titulo = height - 40

    # Dibujar el texto centrado
    pdf.drawCentredString(x_titulo, y_titulo, titulo)

    # Calcular el ancho del texto para subrayado
    titulo_ancho = pdf.stringWidth(titulo, "Helvetica-Bold", 14)

    # Dibujar una línea debajo del texto (subrayado)
    pdf.line(x_titulo - titulo_ancho / 2, y_titulo - 2, x_titulo + titulo_ancho / 2, y_titulo - 2)

    # Definir coordenadas y tamaños
    x_start = 25
    y_start = height - 70
    row_height = 20
    col_widths = [100, 120, 120, 60, 55, 55, 55]  # Anchos de columnas
    x_positions = [x_start + sum(col_widths[:i]) for i in range(len(col_widths))]

    # Agrupar por colaborador
    grouped_by_collaborator = defaultdict(list)
    for obj in queryset:
        grouped_by_collaborator[obj.collaborator].append(obj)

    # Inicializar variables para los totales
    total_tarifa = 0
    total_pagado = 0
    total_saldo = 0

    # Dibujar filas de datos por cada colaborador
    pdf.setFont("Helvetica", 10)
    y = y_start  # Posición inicial para cada colaborador

    for collaborator, items in grouped_by_collaborator.items():
        # Nombre del colaborador (encabezado por colaborador)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x_start, y, f"Colaborador: {collaborator}")
        y -= row_height  # Espacio para separar de los datos

        # Cabecera de la tabla para cada colaborador
        pdf.setFont("Helvetica-Bold", 10)
        headers = ["Fecha", "Colaborador", "Tarea", "Cancelada", "Tarifa", "Pagado", "Saldo"]
        for i, header in enumerate(headers):
            x_centered = x_positions[i] + (col_widths[i] / 2)
            pdf.drawCentredString(x_centered, y - 15, header)  # Texto centrado en celda
            pdf.rect(x_positions[i], y - row_height, col_widths[i], row_height, stroke=1, fill=0)  # Borde de celda
        y -= row_height  # Mover hacia abajo después del encabezado

        # Dibujar las filas de datos para cada colaborador
        pdf.setFont("Helvetica", 10)
        for obj in items:
            values = [
                obj.date.strftime('%A %d/%m/%Y').capitalize(),
                str(obj.collaborator),
                str(obj.task),
                "Sí" if obj.is_paid else "No",
                f"S/. {obj.total_net:.2f}",  # Formato monetario
                f"S/. {obj.paid:.2f}",
                f"S/. {obj.total_net - obj.paid:.2f}",
            ]

            # Calcular los totales
            total_tarifa += obj.total_net
            total_pagado += obj.paid
            total_saldo += (obj.total_net - obj.paid)

            for i, value in enumerate(values):
                if i in [0, 3]:  # Centrar
                    x_centered = x_positions[i] + (col_widths[i] / 2)
                    pdf.drawCentredString(x_centered, y - 15, value)
                elif i in [4, 5, 6]:  # Alinear a la derecha
                    x_right = x_positions[i] + col_widths[i] - 5
                    pdf.drawRightString(x_right, y - 15, value)
                else:  # Alineación por defecto(a la izquierda)
                    x_left = x_positions[i] + 5
                    pdf.drawString(x_left, y - 15, value)

                # Dibuja el borde de la celda
                pdf.rect(x_positions[i], y - row_height, col_widths[i], row_height, stroke=1, fill=0)  # Borde de celda

            y -= row_height  # Mover a la siguiente fila

        # Dibujar la fila de totales para este colaborador
        pdf.setFont("Helvetica-Bold", 10)
        footer_values = [
            "",  # Vacío para la columna "Fecha"
            "",  # Vacío para la columna "Colaborador"
            "",  # Vacío para la columna "Tarea"
            "Total",  # Vacío para la columna "Total"
            f"S/. {total_tarifa:.2f}",  # Total "Tarifa"
            f"S/. {total_pagado:.2f}",  # Total "Pagado"
            f"S/. {total_saldo:.2f}",  # Total "Saldo"
        ]

        # Dibujar el pie de página para este colaborador
        for i, value in enumerate(footer_values):
            if i in [4, 5, 6]:  # Alinear los totales a la derecha
                x_right = x_positions[i] + col_widths[i] - 5
                pdf.drawRightString(x_right, y - 15, value)  # Alinear a la derecha
            else:  # Centrar los valores vacíos en las otras columnas
                x_centered = x_positions[i] + (col_widths[i] / 2)
                pdf.drawCentredString(x_centered, y - 15, value)  # Centrado

            # Dibuja el borde de la celda
            if i in [3, 4, 5, 6]:
                pdf.rect(x_positions[i], y - row_height, col_widths[i], row_height, stroke=1, fill=0)  # Borde de celda

        y -= row_height  # Mover a la siguiente fila para el siguiente colaborador

        # Resetear los totales para el siguiente colaborador
        total_tarifa = 0
        total_pagado = 0
        total_saldo = 0

        # Añadir un espacio entre colaboradores
        y -= row_height  # Dejar espacio entre secciones de colaboradores

    # Finalizar el documento PDF
    pdf.showPage()
    pdf.save()
    return response

exp_pdf_workingday.short_description = "Exportar a PDF"

# FORMS
class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = '__all__'
        
    class Media:
        js = ('js/saleproduct.js',) 
            
    def clean_charged(self):
        charged = self.cleaned_data.get("charged")
        total = self.cleaned_data.get("total")

        if charged and total and charged > total:
            raise ValidationError("El monto cobrado no puede ser mayor que el total.")

        return charged

class WorkingDayForm(forms.ModelForm):
    class Meta:
        model = WorkingDay
        fields = '__all__'
        
    class Media:
        js = ('js/workingday.js',) 


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        
    class Media:
        js = ('js/purchase.js',) 
        
class ToolMaintenanceForm(forms.ModelForm):
    class Meta:
        model = ToolMaintenance
        fields = '__all__'
        
    class Media:
        js = ('js/toolmaintenance.js',) 
               
## INLINES
class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1  # Número de filas vacías
    verbose_name = "Articulo"
    
# PAGES
admin.site.unregister(Group)

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
    list_display = ('name', 'tariff_per_day')
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'um', 'stock', 'type')
    search_fields = ('name',)
    list_filter = ('type',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    form = PurchaseForm 
    fields = ['date', 'provider', 'total', 'is_paid', 'paid']
    list_display = ('provider', 'date_format', 'total_format', 'paid_format', 'balance', 'get_details_names', 'delete_link')
    search_fields = ('provider__name',)
    list_filter = ('provider','date',)
    # readonly_fields= ("total",)
    inlines = [PurchaseDetailInline]
    list_per_page = 20
    ordering = ['-date']  
    actions = None 
    
    @admin.display(description='Total')
    def total_format(self, obj):
        return locale.currency(obj.total, grouping=True)

    @admin.display(description='Pagado')
    def paid_format(self, obj):
        return locale.currency(obj.paid, grouping=True)
    
    @admin.display(description='Pendiente')
    def balance(self, obj):
        balance = (obj.total or 0) - (obj.paid or 0)
        return locale.currency(balance, grouping=True)  
    
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
            
            total_net = locale.currency(sum(item.total or 0 for item in queryset), grouping=True)
            total_paid =  locale.currency(sum(item.paid or 0 for item in queryset), grouping=True)
            total_balance = locale.currency(total_balance_, grouping=True)
            
            extra_context = extra_context or {}
            extra_context['total_net'] = total_net
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
    list_display = ('purchase', 'article', 'unit_cost', 'units', 'charge')
    search_fields = ('article__name', 'purchase__provider')

@admin.register(ToolMaintenance)
class ToolMaintenanceAdmin(admin.ModelAdmin):
    form = ToolMaintenanceForm
    list_display = ('workshop', 'date_format', 'article', 'desc', 'cost_format', 'paid_format', 'balance', 'is_paid','delete_link')
    search_fields = ('workshop__name', 'article__name')
    list_filter = ('workshop', 'article', 'is_paid')
    list_per_page = 20
    ordering = ['-date']  
    actions = None 
    
    @admin.display(description='Tarifa')
    def cost_format(self, obj):
        return locale.currency(obj.cost, grouping=True)

    @admin.display(description='Pagado')
    def paid_format(self, obj):
        return locale.currency(obj.paid, grouping=True)
    
    @admin.display(description='Pendiente')
    def balance(self, obj):
        balance = (obj.cost or 0) - (obj.paid or 0)
        return locale.currency(balance, grouping=True)  
       
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data'):
            cl = self.get_changelist_instance(request)  # Obtiene la lista filtrada
            queryset = cl.get_queryset(request)  # Aplica los filtros activos

            # calcular balance
            total_balance_ = sum(
                (item.cost or 0) - (item.paid or 0) 
                for item in queryset
            )
            
            total_cost = locale.currency(sum(item.cost or 0 for item in queryset), grouping=True)
            total_paid =  locale.currency(sum(item.paid or 0 for item in queryset), grouping=True)
            total_balance = locale.currency(total_balance_, grouping=True)

            extra_context = extra_context or {}
            extra_context['total_cost'] = total_cost
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

@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    form = WorkingDayForm
    fields = ['date', 'collaborator', 'task','total_net','is_paid', 'paid',]
    list_display = ('collaborator', 'date_format','task','total_net_format', 'paid_format', 'balance', 'is_paid', 'delete_link')
    search_fields = ('collaborator__firstname', 'task__name',)
    list_filter = ('date', ('collaborator', RelatedOnlyFieldListFilter), 'task', 'is_paid')
    list_per_page = 20
    ordering = ['-date']  
    actions = [exp_pdf_workingday] 
    
    @admin.display(description='Tarifa')
    def total_net_format(self, obj):
        return locale.currency(obj.total_net, grouping=True)

    @admin.display(description='Pagado')
    def paid_format(self, obj):
        return locale.currency(obj.total_net, grouping=True)
    
    @admin.display(description='Saldo')
    def balance(self, obj):
        balance = (obj.total_net or 0) - (obj.paid or 0)
        return locale.currency(balance, grouping=True)
    
    @admin.display(description='Fecha')
    def date_format(self, obj):
        return obj.date.strftime('%A %d/%m/%Y').capitalize()
    date_format.admin_order_field = 'date'
    
    def changelist_view(self, request, extra_context=None):
            response = super().changelist_view(request, extra_context=extra_context)

            if hasattr(response, 'context_data'):
                cl = self.get_changelist_instance(request)  # Obtiene la lista filtrada
                queryset = cl.get_queryset(request)  # Aplica los filtros activos

                # calcular total pago neto
                total_net = sum(
                    (item.total_net or 0)
                    for item in queryset
                )
  
                total_paid = sum(item.paid or 0 for item in queryset)
                
                total_balance_ = sum(
                    (item.total_net or 0) - (item.paid or 0) 
                    for item in queryset
                )
                
                total_net = locale.currency(sum(item.total_net or 0 for item in queryset), grouping=True)
                total_paid =  locale.currency(sum(item.paid or 0 for item in queryset), grouping=True)
                total_balance = locale.currency(total_balance_, grouping=True)

                extra_context = extra_context or {}
                extra_context['total_net'] = total_net
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

@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    form = SaleProductForm
    fields = ["date", "client", "units", "price_unit", "total_net", "is_paid", "paid"]
    list_display = ('client', 'date_format','units', 'price_unit', 'total_net_format', 'paid_format', 'balance', 'is_paid','delete_link')
    search_fields = ('client__name', )
    list_filter = ('client', 'date', 'is_paid')
    list_per_page = 20
    ordering = ['-date']  
    actions = None
    
    @admin.display(description='Tarifa')
    def total_net_format(self, obj):
        return locale.currency(obj.total_net, grouping=True)

    @admin.display(description='Pagado')
    def paid_format(self, obj):
        return locale.currency(obj.paid, grouping=True)
    
    @admin.display(description='Pendiente')
    def balance(self, obj):
        balance = (obj.total_net or 0) - (obj.paid or 0)
        return locale.currency(balance, grouping=True)  
     
    @admin.display(description='Fecha')
    def date_format(self, obj):
        return obj.date.strftime('%A %d/%m/%Y').capitalize()
    date_format.admin_order_field = 'date'
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data'):
            cl = self.get_changelist_instance(request)  # Obtiene la lista filtrada
            queryset = cl.get_queryset(request)  # Aplica los filtros activos

            total_balance_ = sum(
                (item.total_net or 0) - (item.paid or 0) 
                for item in queryset
            )
            
            total_net = locale.currency(sum(item.total_net or 0 for item in queryset), grouping=True)
            total_paid =  locale.currency(sum(item.paid or 0 for item in queryset), grouping=True)
            total_balance = locale.currency(total_balance_, grouping=True)
            

            extra_context = extra_context or {}
            extra_context['total_net'] = total_net
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
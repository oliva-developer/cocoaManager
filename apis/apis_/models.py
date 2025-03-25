from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User, AbstractUser

class Collaborator(models.Model):
    firstname = models.CharField(max_length=100, verbose_name="Nombres")
    lastname = models.CharField(max_length=100, verbose_name="Apellidos")
    phone = models.CharField(max_length=15, verbose_name="Celular")

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    pay_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pago por día")

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        
    def __str__(self):
        return self.name

class Article(models.Model):
    TYPE_CHOICES = [
        ('product', 'Producto'),
        ('tool', 'Herramienta'),
    ]
    name = models.CharField(max_length=255, verbose_name="Nombre")
    um = models.CharField(max_length=50, verbose_name="Unidad de Medida")  # Unidad de medida
    stock = models.PositiveIntegerField(verbose_name="Existencias")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='product', verbose_name="Tipo")

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
class Purchase(models.Model):
    provider = models.CharField(max_length=100, verbose_name="Proveedor")
    date = models.DateTimeField(default=now, verbose_name="Fecha de compra")
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto Pagado")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto Total")
    is_paid = models.BooleanField(default=True, verbose_name="Pagado")

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        
    def __str__(self):
        return f"Compra de {self.provider} el {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    
class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='details', verbose_name="Compra")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="purchases", verbose_name="Articulo")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario")
    units = models.IntegerField(verbose_name="Cantidad")
    
    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compras"

    def __str__(self):
        return f"{self.units} x {self.article.name} en {self.purchase}"
    
class ToolMaintenance (models.Model):
    provider = models.CharField(max_length=100,blank=True, null=True, verbose_name="Técnico")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Herramienta")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo")
    date = models.DateTimeField(default=now, verbose_name="Fecha de Reparación")
    
    class Meta:
        verbose_name = "Mantenimiento de Herramienta"
        verbose_name_plural = "Mantenimientos de Herramientas"
        
    def __str__(self):
        return f"{self.article} atendido por {self.provider}"
    
class WorkingDay(models.Model):
    collaborator = models.ForeignKey(Collaborator, on_delete=models.CASCADE, verbose_name="Colaborador")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Tarea")
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Descuento")
    pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Pago")
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto Pagado")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto Pendiente")
    use_own_tool = models.BooleanField(default=True, verbose_name="Usa Herramienta Propia")
    tool_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Descuento por herramienta")
    is_done = models.BooleanField(default=False, verbose_name="Concluida")
    is_canceled = models.BooleanField(default=False, verbose_name="Cancelada")
    observation = models.TextField(null=True, blank=True, verbose_name="Observacion")
    date = models.DateTimeField(default=now, verbose_name="Fecha de Jornada")

    class Meta:
        verbose_name = "Jornada de Trabajo"
        verbose_name_plural = "Jornadas de Trabajo"
        
    def __str__(self):
        return f"{self.collaborator} - {self.task} ({self.date.strftime('%Y-%m-%d')})"

class WorkingDayResource(models.Model):
    working_day = models.ForeignKey(WorkingDay, on_delete=models.CASCADE, verbose_name="Jornada laboral")
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Recurso")
    units = models.IntegerField(verbose_name="Cantidad")
    
    class Meta:
        verbose_name = "Recurso de Jornada de Trabajo"
        verbose_name_plural = "Recursos de Jornadas de Trabajo"
        
    def __str__(self):
        return f"En {self.working_day} se uso {self.units} de {self.article}"
    
class SaleProduct(models.Model):
    client = models.CharField(max_length=100, verbose_name="Cliente", default="Ninguno")
    kilos = models.IntegerField(default=1, verbose_name="kilos")
    price_kilo = models.DecimalField(max_digits=18, decimal_places=2, default=1.00, verbose_name="Precio de Kilo")
    total = models.DecimalField(max_digits=18, decimal_places=2, default=1.00, verbose_name="Monto")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Descuento")
    
    class Meta:
        verbose_name = "Venta de Producto"
        verbose_name_plural = "Ventas de Producto"
        
    def __str__(self):
        return f"A {self.client} se vendio {self.kilos} kilos de cacao por un total de {self.total} soles"

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"  
        
    def __str__(self):
        return f"{self.username}"
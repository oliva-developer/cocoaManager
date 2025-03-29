from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User, AbstractUser
from decimal import Decimal
    
class Person(models.Model):
    firstname = models.CharField(max_length=100, verbose_name="Nombres")
    lastname = models.CharField(max_length=100, verbose_name="Apellidos")
    phone = models.CharField(max_length=15, verbose_name="Celular")
    address = models.CharField(max_length=50, null= True, blank=True,verbose_name="Dirección")
    
    class Meta:
        abstract = True
        
class Entity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    phone = models.CharField(max_length=15, verbose_name="Celular")
    city = models.CharField(max_length=50, null= True, blank=True,verbose_name="Ciudad")
    
    class Meta:
        abstract = True
    
class Collaborator(Person):
    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Customer(Entity):
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes" 
        
    def __str__(self):
        return f"{self.name}"
         
class Provider(Entity):
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"  
        
    def __str__(self):
        return f"{self.name}"
    
class Workshop(Entity):
    class Meta:
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"  
        
    def __str__(self):
        return f"{self.name}"
    
class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    tariff_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Tarifa diaria")

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        
    def __str__(self):
        return f"{self.name}"

class Article(models.Model):
    TYPE_CHOICES = [
        ('product', 'Producto'),
        ('tool', 'Herramienta'),
    ]
    name = models.CharField(max_length=255, verbose_name="Nombre")
    um = models.CharField(max_length=50, verbose_name="Unidad de Medida")  # Unidad de medida
    stock = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"),verbose_name="Existencias")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='product', verbose_name="Tipo")

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
class Purchase(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True, related_name='Sales', verbose_name="Proveedor")    
    date = models.DateField(default=now, verbose_name="Fecha")
    total = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"), verbose_name="Total")
    is_paid = models.BooleanField(default=False, verbose_name="Cancelada")
    paid = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"), verbose_name="Pagado")

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        
    def __str__(self):
        return f"Compra de {self.provider} el {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    
class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='details', verbose_name="Compra")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="purchases", verbose_name="Artículo")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario")
    units = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    charge = models.DecimalField(max_digits=10, decimal_places=2, default= Decimal("0.00"), verbose_name="Importe")
    
    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compras"

    def __str__(self):
        return f"{self.units} x {self.article.name} en {self.purchase}"
    
class ToolMaintenance (models.Model):
    date = models.DateField(default=now, verbose_name="Fecha")
    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, null=True, blank=True,related_name='maintenances', verbose_name="Taller")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Herramienta")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="Detalle")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo")
    is_paid = models.BooleanField(default=False, verbose_name="Cancelado")
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Pagado")
    
    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        
    def __str__(self):
        return f"{self.article} atendido por {self.workshop}"
    
class WorkingDay(models.Model):
    date = models.DateField(default=now, verbose_name="Fecha")
    collaborator = models.ForeignKey(Collaborator, on_delete=models.SET_NULL, null=True, blank=True, related_name="workingdays",verbose_name="Colaborador")
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name="workings",verbose_name="Tarea")
    total_net = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Tarifa S/")
    is_paid = models.BooleanField(default=False, verbose_name="Cancelada")
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Pagado S/")

    class Meta:
        verbose_name = "Jornada Laboral"
        verbose_name_plural = "Jornadas Laborales"
        
    def __str__(self):
        return f"{self.collaborator}  {self.task} {self.date.strftime('%Y-%m-%d')}"
    
class SaleProduct(models.Model):
    date = models.DateField(default=now, verbose_name="Fecha")
    client = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='shoppings', verbose_name="Cliente")
    units = models.DecimalField(max_digits=18, decimal_places=3, default=Decimal("0.00"), verbose_name="Cantidad (Kilos)")
    price_unit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"), verbose_name="Precio (Kilo) S/")
    total_net = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"), verbose_name="Generado S/")
    is_paid = models.BooleanField(default=False, verbose_name="Cancelada")
    paid = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"), verbose_name="Ingresado S/")
    observation = models.CharField(max_length=200,blank=True, null=True, verbose_name="Observación")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        
    def __str__(self):
        return f"A {self.client} se vendio {self.kilos} kilos de cacao por un total de {self.total} soles"

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"  
        
    def __str__(self):
        return f"{self.username}"

class Kpi(models.Model):
    name = models.CharField(max_length=20,null=True, blank=True)
    
    class Meta:
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadores"  
        
    def __str__(self):
        return f"{self.name}"
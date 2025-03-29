# Generated by Django 5.1.7 on 2025-03-29 03:28

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis_', '0002_alter_workingday_collaborator_alter_workingday_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saleproduct',
            old_name='kilos',
            new_name='units',
        ),
        migrations.RemoveField(
            model_name='saleproduct',
            name='charged',
        ),
        migrations.RemoveField(
            model_name='saleproduct',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='saleproduct',
            name='discount_reazon',
        ),
        migrations.RemoveField(
            model_name='saleproduct',
            name='price_kilo',
        ),
        migrations.RemoveField(
            model_name='saleproduct',
            name='total',
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='observation',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Observación'),
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=18, verbose_name='Pagado S/'),
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='price_unit',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=18, verbose_name='Precio (Kilo) S/'),
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='total_net',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=18, verbose_name='Valor Monetario: S/'),
        ),
    ]

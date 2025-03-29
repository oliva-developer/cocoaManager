# Generated by Django 5.1.7 on 2025-03-29 04:10

import django.utils.timezone
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis_', '0003_rename_kilos_saleproduct_units_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Cancelada'),
        ),
        migrations.AlterField(
            model_name='saleproduct',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='saleproduct',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Cancelada'),
        ),
        migrations.AlterField(
            model_name='saleproduct',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=18, verbose_name='Valor Recepcionado S/'),
        ),
        migrations.AlterField(
            model_name='saleproduct',
            name='total_net',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=18, verbose_name='Valor Establecido: S/'),
        ),
        migrations.AlterField(
            model_name='saleproduct',
            name='units',
            field=models.DecimalField(decimal_places=3, default=Decimal('0.00'), max_digits=18, verbose_name='Cantidad (Kilos)'),
        ),
        migrations.AlterField(
            model_name='workingday',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Cancelada'),
        ),
    ]

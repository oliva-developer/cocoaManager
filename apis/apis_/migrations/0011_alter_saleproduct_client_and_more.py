# Generated by Django 5.1.7 on 2025-03-26 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis_', '0010_toolmaintenance_desc_toolmaintenance_is_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleproduct',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shoppings', to='apis_.customer', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='toolmaintenance',
            name='technical',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenances', to='apis_.technical', verbose_name='Técnico'),
        ),
    ]

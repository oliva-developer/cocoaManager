# Generated by Django 5.1.7 on 2025-03-25 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis_', '0006_alter_purchase_provider_alter_saleproduct_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='is_paid',
            field=models.BooleanField(default=True, verbose_name='Pagado'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Monto Pagado'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Monto Total'),
        ),
    ]

# Generated by Django 5.1.7 on 2025-03-25 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis_', '0004_alter_purchasedetail_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingday',
            name='is_done',
            field=models.BooleanField(default=False, verbose_name='Concluida'),
        ),
    ]

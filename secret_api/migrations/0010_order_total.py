# Generated by Django 5.0.1 on 2024-01-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_api', '0009_alter_order_idcustomer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-15 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_api', '0005_remove_customer_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sword',
            name='completed',
            field=models.CharField(max_length=180),
        ),
    ]
# Generated by Django 5.0.1 on 2024-01-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_api', '0011_gun_sword_sharpness'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]

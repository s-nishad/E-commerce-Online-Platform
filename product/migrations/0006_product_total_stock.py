# Generated by Django 5.1.2 on 2024-10-29 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_product_total_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-29 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_stock_stock_stock_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='stock',
            new_name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='total_stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='stock_type',
            field=models.CharField(choices=[('IN', 'In'), ('OUT', 'Out')], default='IN', max_length=3),
        ),
    ]
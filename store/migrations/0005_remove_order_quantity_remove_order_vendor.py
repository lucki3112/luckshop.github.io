# Generated by Django 4.1.7 on 2023-03-24 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_products_api_carts_api_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='vendor',
        ),
    ]

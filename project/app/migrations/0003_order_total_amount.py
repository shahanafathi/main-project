# Generated by Django 5.0.6 on 2024-07-23 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_order_cart_id_order_payment_status_wishlist_cart_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

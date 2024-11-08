# Generated by Django 5.1 on 2024-11-07 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_contactus_customeuser_delivery_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='per_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]

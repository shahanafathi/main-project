# Generated by Django 5.1 on 2024-09-29 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_cart_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.AddField(
            model_name='medicine',
            name='category_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

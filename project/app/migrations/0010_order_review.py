# Generated by Django 5.0.6 on 2024-08-08 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_order_payment_status_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='order_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, max_length=100, null=True)),
                ('rating', models.PositiveIntegerField(default=5)),
                ('Image', models.FileField(blank=True, null=True, upload_to='')),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('medicine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.medicine')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

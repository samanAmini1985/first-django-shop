# Generated by Django 4.2.3 on 2023-07-30 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_coupon_order_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]

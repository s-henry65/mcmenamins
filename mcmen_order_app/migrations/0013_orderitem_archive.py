# Generated by Django 4.0.1 on 2022-09-27 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_order_app', '0012_orderitemcount_orderitem_keg_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='archive',
            field=models.BooleanField(default=False),
        ),
    ]
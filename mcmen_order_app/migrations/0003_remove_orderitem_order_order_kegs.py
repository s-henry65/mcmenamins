# Generated by Django 4.0.1 on 2022-08-16 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_order_app', '0002_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='kegs',
            field=models.ManyToManyField(blank=True, null=True, to='mcmen_order_app.OrderItem'),
        ),
    ]

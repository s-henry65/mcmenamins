# Generated by Django 4.0.1 on 2022-08-21 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_order_app', '0003_remove_orderitem_order_order_kegs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='kegs',
            field=models.ManyToManyField(to='mcmen_order_app.OrderItem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=10),
        ),
    ]
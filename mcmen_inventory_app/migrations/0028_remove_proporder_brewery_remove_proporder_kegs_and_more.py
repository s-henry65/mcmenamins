# Generated by Django 4.0.1 on 2022-08-16 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_inventory_app', '0027_brewery_inv_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proporder',
            name='brewery',
        ),
        migrations.RemoveField(
            model_name='proporder',
            name='kegs',
        ),
        migrations.RemoveField(
            model_name='proporder',
            name='property',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='PropOrder',
        ),
    ]

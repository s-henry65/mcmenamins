# Generated by Django 4.0.1 on 2022-09-13 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_inventory_app', '0035_comingsoon_brewery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comingsoon',
            name='description',
            field=models.CharField(max_length=75),
        ),
    ]

# Generated by Django 4.0.1 on 2022-05-19 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_inventory_app', '0002_alter_brewer_options_alter_brewery_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brewery',
            name='phone_num',
            field=models.CharField(max_length=10),
        ),
    ]
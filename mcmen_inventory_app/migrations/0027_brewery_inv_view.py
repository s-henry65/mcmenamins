# Generated by Django 4.0.1 on 2022-07-25 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_inventory_app', '0026_remove_brewery_brewers_delete_brewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewery',
            name='inv_view',
            field=models.CharField(default='Graphic', max_length=10),
        ),
    ]
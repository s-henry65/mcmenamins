# Generated by Django 4.0.1 on 2022-09-27 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_inventory_app', '0037_rename_category_kegs_sku'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comingsoon',
            old_name='category',
            new_name='sku',
        ),
    ]
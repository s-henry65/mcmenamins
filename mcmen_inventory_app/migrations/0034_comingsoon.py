# Generated by Django 4.0.1 on 2022-09-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_inventory_app', '0033_rename_postcomment_brewlogcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComingSoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beer', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=20)),
                ('finish_date', models.DateField()),
                ('description', models.CharField(max_length=100)),
            ],
        ),
    ]

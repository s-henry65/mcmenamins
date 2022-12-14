# Generated by Django 4.0.1 on 2022-08-16 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mcmen_inventory_app', '0028_remove_proporder_brewery_remove_proporder_kegs_and_more'),
        ('mcmen_dist_app', '0025_alter_article_pub_date_alter_postcomment_author_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField()),
                ('order_date', models.DateField()),
                ('updated', models.DateField(auto_now=True)),
                ('status', models.CharField(default='Pending', max_length=10)),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mcmen_inventory_app.kegs')),
                ('brewery', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brewery', to='mcmen_inventory_app.brewery')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mcmen_dist_app.property')),
            ],
            options={
                'ordering': ('order_date',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField()),
                ('complete', models.BooleanField(default=False)),
                ('updated', models.DateField(auto_now=True)),
                ('status', models.CharField(default='Open', max_length=10)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mcmen_dist_app.property')),
            ],
            options={
                'ordering': ('order_date',),
            },
        ),
    ]

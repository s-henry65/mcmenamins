# Generated by Django 4.0.1 on 2022-09-09 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_user_app', '0003_userprofile_view_pref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='job_title',
            field=models.CharField(max_length=30),
        ),
    ]

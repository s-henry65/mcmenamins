# Generated by Django 4.0.1 on 2022-08-29 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_user_app', '0002_remove_userprofile_nick_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='view_pref',
            field=models.CharField(default='Graph', max_length=20),
        ),
    ]

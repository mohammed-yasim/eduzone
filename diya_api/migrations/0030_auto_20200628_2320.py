# Generated by Django 3.0.5 on 2020-06-28 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diya_api', '0029_auto_20200628_2319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='userlimit',
            new_name='quota',
        ),
    ]

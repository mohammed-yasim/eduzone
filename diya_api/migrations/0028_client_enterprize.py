# Generated by Django 3.0.5 on 2020-06-28 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diya_api', '0027_auto_20200628_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='enterprize',
            field=models.BooleanField(default=False, verbose_name='Enterprize Subscriber'),
        ),
    ]

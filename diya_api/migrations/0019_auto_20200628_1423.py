# Generated by Django 3.0.5 on 2020-06-28 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diya_api', '0018_channel_enterprize'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='password',
            field=models.CharField(default='eduzone', max_length=64, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=models.CharField(default=0, max_length=10, verbose_name='Mobile Number'),
        ),
    ]

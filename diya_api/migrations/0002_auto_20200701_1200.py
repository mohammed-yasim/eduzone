# Generated by Django 3.0.5 on 2020-07-01 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diya_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='video',
            field=models.ManyToManyField(blank=True, related_name='playlist', to='diya_api.Video', verbose_name='Videos'),
        ),
    ]

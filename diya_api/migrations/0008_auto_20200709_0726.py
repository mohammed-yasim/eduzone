# Generated by Django 3.0.5 on 2020-07-09 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diya_api', '0007_elogin_ewatch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ewatch',
            name='datetime',
            field=models.DateTimeField(auto_now=True, verbose_name='Date time'),
        ),
        migrations.AlterField(
            model_name='ewatch',
            name='euser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched', to='diya_api.Esubscibers', verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='ewatch',
            name='url',
            field=models.TextField(blank=True, default=0, verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='ewatch',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diya_api.Video', verbose_name='Watched'),
        ),
    ]

# Generated by Django 3.0.5 on 2020-06-28 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diya_api', '0021_video_client'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-date'], 'verbose_name': 'Video/Topic/Lesson', 'verbose_name_plural': 'Videos/Topics/Lesson'},
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0009_channel_thumbnail_url_alter_channel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='custom_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

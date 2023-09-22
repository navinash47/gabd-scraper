# Generated by Django 4.2.5 on 2023-09-21 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0006_channel_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-published_at']},
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
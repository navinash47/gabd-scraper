# Generated by Django 4.2.5 on 2023-09-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0002_alter_video_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branddeal',
            name='final_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='branddeal',
            name='initial_url',
            field=models.TextField(),
        ),
    ]

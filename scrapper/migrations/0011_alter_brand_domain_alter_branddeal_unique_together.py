# Generated by Django 4.2.5 on 2023-09-23 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0010_alter_channel_custom_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='domain',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='branddeal',
            unique_together={('video', 'initial_url')},
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-19 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='status',
        ),
        migrations.AlterField(
            model_name='branddeal',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_deals', to='scrapper.video'),
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(choices=[('S', 'Scraped'), ('D', 'Detailed'), ('F', 'Filtered')], default='S', max_length=1),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-20 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0004_remove_video_dislike_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branddeal',
            old_name='url',
            new_name='initial_url',
        ),
        migrations.AddField(
            model_name='branddeal',
            name='final_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='branddeal',
            name='status',
            field=models.CharField(choices=[('I', 'Initial'), ('S', 'Scraped')], default='I', max_length=1),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='branddeal',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_deals', to='scrapper.brand'),
        ),
    ]
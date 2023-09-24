# Generated by Django 4.2.5 on 2023-09-24 13:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0011_alter_brand_domain_alter_branddeal_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('domain', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]
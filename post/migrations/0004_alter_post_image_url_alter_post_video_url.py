# Generated by Django 5.0.3 on 2024-05-18 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_url',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='video_url',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
# Generated by Django 5.0.3 on 2024-05-18 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_useraccount_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='dp',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2020-12-12 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201212_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]

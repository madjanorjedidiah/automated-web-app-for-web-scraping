# Generated by Django 3.0.6 on 2020-05-30 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agg', '0003_auto_20200530_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estates',
            name='beds',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='estates',
            name='garages',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='estates',
            name='showers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
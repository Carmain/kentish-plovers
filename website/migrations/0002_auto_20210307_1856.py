# Generated by Django 3.1.6 on 2021-03-07 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plover',
            name='banding_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Banding year'),
        ),
    ]

# Generated by Django 3.1 on 2021-04-08 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medrec_v2', '0003_remove_medication_trade_name_regex'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='trade_name_regex',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]

# Generated by Django 3.1 on 2020-08-26 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meddatabase', '0003_med_brand_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='med',
            options={'ordering': ['medication_name']},
        ),
    ]
# Generated by Django 3.1 on 2021-04-08 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medrec_v2', '0004_medication_trade_name_regex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instlookup',
            options={'ordering': ['inst_num']},
        ),
        migrations.RenameField(
            model_name='siglookup',
            old_name='sig_desc',
            new_name='sig_plain_text',
        ),
    ]

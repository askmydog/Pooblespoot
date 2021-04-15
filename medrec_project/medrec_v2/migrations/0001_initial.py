# Generated by Django 3.1 on 2021-04-07 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_med_name', models.CharField(max_length=200, unique=True, verbose_name='Base Medication Name')),
                ('base_med_add_terms', models.CharField(blank=True, help_text='Enter any abbreviations used for the medication. Ex: HCT, HCTZ for Hydrochlorothiazide', max_length=200, verbose_name='Search Terms')),
                ('base_med_regex', models.CharField(blank=True, max_length=200)),
                ('base_med_pronun', models.CharField(blank=True, max_length=200, verbose_name='Medication Pronunciation')),
                ('base_med_notes', models.CharField(blank=True, max_length=400)),
            ],
            options={
                'ordering': ['base_med_name'],
            },
        ),
        migrations.CreateModel(
            name='DateLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_num', models.IntegerField()),
                ('date_regex', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='DoseLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dose_num', models.IntegerField()),
                ('dose_regex', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='InstLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inst_num', models.IntegerField()),
                ('inst_regex', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='MedInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('med_input', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MedQualifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qual_name', models.CharField(max_length=50)),
                ('qual_desc', models.CharField(blank=True, max_length=200)),
                ('qual_add_terms', models.CharField(blank=True, help_text='Enter any additional search terms for this qualifier', max_length=200, verbose_name='Additional Search Terms')),
                ('qual_regex', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ['qual_name'],
            },
        ),
        migrations.CreateModel(
            name='MedRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_name', models.CharField(max_length=50)),
                ('route_desc', models.CharField(blank=True, max_length=200)),
                ('route_add_term', models.CharField(max_length=200)),
                ('route_regex', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SigLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sig_name', models.CharField(max_length=200)),
                ('sig_desc', models.CharField(blank=True, max_length=200)),
                ('sig_add_term', models.CharField(max_length=200)),
                ('sig_regex', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MedType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=200)),
                ('type_desc', models.CharField(blank=True, max_length=200)),
                ('type_interact', models.ManyToManyField(blank=True, related_name='_medtype_type_interact_+', to='medrec_v2.MedType')),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_name', models.CharField(blank=True, help_text='Separate multiple trade names with a comma.  Ex: Advil, Motrin', max_length=200, verbose_name='Trade Name')),
                ('med_add_terms', models.CharField(blank=True, help_text='Add any additional search terms that will help differentiate this medication from other similar medications.  Ex: 25mg for Viagra (Sildenifil), 10mg for Rovatio (Sildenifil)', max_length=200, verbose_name='Additional Regular Expression Search Terms')),
                ('display_name', models.CharField(blank=True, default='', help_text='Automatically generated name based on the trade name and generic medications selected.', max_length=200, verbose_name='Display Name')),
                ('custom_disp_name', models.CharField(blank=True, default='', help_text='Enter a different custom name if the autmomatically generated name is not formatted correctly.  Be sure to update if any medications are made to the medications.', max_length=200, verbose_name='Custom Trade Name')),
                ('med_commonuses', models.CharField(blank=True, default='', help_text="Add the common uses for this medication. Ex: enter 'Pain' for Tylenol", max_length=200, verbose_name='Common medication uses')),
                ('med_notes', models.CharField(blank=True, default='', max_length=200)),
                ('med_1', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='med_1', to='medrec_v2.basemed')),
                ('med_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='med_2', to='medrec_v2.basemed')),
                ('med_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='med_3', to='medrec_v2.basemed')),
                ('med_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='med_4', to='medrec_v2.basemed')),
                ('med_qualifiers', models.ManyToManyField(blank=True, help_text='Select any characteristics specific to this formulation of the  medication. Ex: Extended Release or lotion', to='medrec_v2.MedQualifier')),
                ('med_route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medrec_v2.medroute', verbose_name='Medication Route')),
            ],
            options={
                'ordering': ['med_1'],
            },
        ),
        migrations.AddField(
            model_name='basemed',
            name='base_med_interactions',
            field=models.ManyToManyField(blank=True, related_name='med_interactions', to='medrec_v2.MedType', verbose_name='Medication Interactions'),
        ),
        migrations.AddField(
            model_name='basemed',
            name='base_med_type',
            field=models.ManyToManyField(blank=True, to='medrec_v2.MedType', verbose_name='Medication Type'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-17 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dpnk', '0005_auto_20160216_1838'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TeamInCampaign',
        ),
        migrations.AddField(
            model_name='campaign',
            name='late_admission_phase',
            field=models.NullBooleanField(default=None, editable=False),
        ),
        migrations.AddField(
            model_name='userattendance',
            name='related_company_admin',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dpnk.CompanyAdmin'),
        ),
        migrations.AddField(
            model_name='userattendance',
            name='representative_payment',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dpnk.Payment'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='personal_data_opt_in',
            field=models.BooleanField(default=False, verbose_name='Souhlas se zpracováním osobních údajů.'),
        ),
    ]

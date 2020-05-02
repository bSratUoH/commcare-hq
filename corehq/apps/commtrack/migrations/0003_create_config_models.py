# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-04 00:23
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commtrack', '0002_stockstate_last_modified_form_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SQLActionConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=40, null=True)),
                ('subaction', models.CharField(max_length=40, null=True)),
                ('_keyword', models.CharField(max_length=40, null=True)),
                ('caption', models.CharField(max_length=40, null=True)),
            ],
            options={
                'db_table': 'commtrack_actionconfig',
            },
        ),
        migrations.CreateModel(
            name='SQLCommtrackConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=126, unique=True)),
                ('couch_id', models.CharField(db_index=True, max_length=126, null=True)),
                ('use_auto_emergency_levels', models.BooleanField(default=False)),
                ('sync_consumption_fixtures', models.BooleanField(default=False)),
                ('use_auto_consumption', models.BooleanField(default=False)),
                ('individual_consumption_defaults', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'commtrack_commtrackconfig',
            },
        ),
        migrations.CreateModel(
            name='SQLAlertConfig',
            fields=[
                ('stock_out_facilities', models.BooleanField(default=False)),
                ('stock_out_commodities', models.BooleanField(default=False)),
                ('stock_out_rates', models.BooleanField(default=False)),
                ('non_report', models.BooleanField(default=False)),
                ('commtrack_config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                          primary_key=True, serialize=False,
                                                          to='commtrack.SQLCommtrackConfig')),
            ],
            options={
                'db_table': 'commtrack_alertconfig',
            },
        ),
        migrations.CreateModel(
            name='SQLConsumptionConfig',
            fields=[
                ('min_transactions', models.IntegerField(default=2, null=True)),
                ('min_window', models.IntegerField(default=10, null=True)),
                ('optimal_window', models.IntegerField(null=True)),
                ('use_supply_point_type_default_consumption', models.BooleanField(default=False)),
                ('exclude_invalid_periods', models.BooleanField(default=False)),
                ('commtrack_config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                          primary_key=True, serialize=False,
                                                          to='commtrack.SQLCommtrackConfig')),
            ],
            options={
                'db_table': 'commtrack_consumptionconfig',
            },
        ),
        migrations.CreateModel(
            name='SQLStockLevelsConfig',
            fields=[
                ('emergency_level', models.DecimalField(decimal_places=2, default=0.5, max_digits=3)),
                ('understock_threshold', models.DecimalField(decimal_places=2, default=1.5, max_digits=3)),
                ('overstock_threshold', models.DecimalField(decimal_places=2, default=3, max_digits=3)),
                ('commtrack_config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                          primary_key=True, serialize=False,
                                                          to='commtrack.SQLCommtrackConfig')),
            ],
            options={
                'db_table': 'commtrack_stocklevelsconfig',
            },
        ),
        migrations.CreateModel(
            name='SQLStockRestoreConfig',
            fields=[
                ('section_to_consumption_types', django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True)),
                ('force_consumption_case_types', django.contrib.postgres.fields.jsonb.JSONField(default=list, null=True)),
                ('use_dynamic_product_list', models.BooleanField(default=False)),
                ('commtrack_config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                          primary_key=True, serialize=False,
                                                          to='commtrack.SQLCommtrackConfig')),
            ],
            options={
                'db_table': 'commtrack_stockrestoreconfig',
            },
        ),
        migrations.AddField(
            model_name='sqlactionconfig',
            name='commtrack_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='commtrack.SQLCommtrackConfig'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='sqlactionconfig',
            order_with_respect_to='commtrack_config',
        ),
    ]

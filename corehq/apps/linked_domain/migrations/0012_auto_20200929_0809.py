# Generated by Django 2.2.16 on 2020-09-29 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linked_domain', '0011_auto_20200728_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainlinkhistory',
            name='model',
            field=models.CharField(choices=[('app', 'Application'), ('custom_user_data', 'Custom User Data Fields'), ('custom_product_data', 'Custom Product Data Fields'), ('custom_location_data', 'Custom Location Data Fields'), ('roles', 'User Roles'), ('toggles', 'Feature Flags and Previews'), ('fixture', 'Lookup Table'), ('case_search_data', 'Case Search Settings'), ('report', 'Report'), ('data_dictionary', 'Data Dictionary'), ('keyword', 'Keyword')], max_length=128),
        ),
    ]
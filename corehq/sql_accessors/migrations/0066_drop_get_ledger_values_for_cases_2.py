from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sql_accessors', '0065_get_ledger_values_for_cases_3'),
    ]

    operations = [
        migrations.RunSQL(
            "DROP FUNCTION IF EXISTS get_ledger_values_for_cases_2(TEXT[], TEXT[], TEXT[], TIMESTAMP, TIMESTAMP);"
        )
    ]
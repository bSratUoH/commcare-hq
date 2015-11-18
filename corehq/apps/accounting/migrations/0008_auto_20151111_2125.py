# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_subscription_funding_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaccount',
            name='last_payment_method',
            field=models.CharField(default=b'NONE', max_length=25, choices=[(b'CC_ONE_TIME', b'Credit Card - One Time'), (b'CC_AUTO', b'Credit Card - Autopay'), (b'WIRE', b'Wire'), (b'ACH', b'ACH'), (b'OTHER', b'Other'), (b'BU_PAYMENT', b'Payment to local BU'), (b'NONE', b'None')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='pro_bono_status',
            field=models.CharField(default=b'FULL_PRICE', max_length=25, choices=[(b'FULL_PRICE', b'Full Price'), (b'DISCOUNTED', b'Discounted'), (b'PRO_BONO', b'Pro Bono')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='service_type',
            field=models.CharField(max_length=25, choices=[(b'IMPLEMENTATION', b'Implementation'), (b'PRODUCT', b'Product'), (b'TRIAL', b'Trial'), (b'SANDBOX', b'Sandbox'), (b'INTERNAL', b'Internal')]),
            preserve_default=True,
        ),
    ]

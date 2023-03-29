# Generated by Django 4.1.7 on 2023-03-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_payment_paypal_transaction_id_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='country_code',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='ticket',
            name='currency',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AddField(
            model_name='ticket',
            name='payer_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='ticket',
            name='time_paid',
            field=models.DateTimeField(null=True),
        ),
    ]

# Generated by Django 4.1.7 on 2023-05-09 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Amount',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]

# Generated by Django 4.2.1 on 2023-07-10 10:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fullcongress', '0002_fullcongressregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='fullcongressregistration',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

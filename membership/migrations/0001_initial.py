# Generated by Django 4.2.1 on 2023-07-11 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('occupation', models.CharField(max_length=100)),
                ('terms_checkbox', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('membership_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.membershipcategory')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=60)),
                ('payment_id', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('payment_status', models.CharField(max_length=30)),
                ('gross_pay', models.DecimalField(decimal_places=2, max_digits=8)),
                ('paypal_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('net_pay', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payer_id', models.CharField(max_length=100)),
                ('membership_registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.membershipregistration')),
                ('registration_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.membershipcategory')),
                ('registration_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.registrationtype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='membershipregistration',
            name='registration_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.registrationtype'),
        ),
        migrations.AddField(
            model_name='membershipregistration',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membershipcategory',
            name='registration_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.registrationtype'),
        ),
    ]

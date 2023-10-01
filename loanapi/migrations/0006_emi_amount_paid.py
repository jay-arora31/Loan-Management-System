# Generated by Django 4.2.5 on 2023-10-01 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanapi', '0005_emi_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='emi',
            name='amount_paid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

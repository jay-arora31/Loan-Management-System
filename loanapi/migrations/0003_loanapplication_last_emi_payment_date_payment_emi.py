# Generated by Django 4.2.5 on 2023-09-30 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loanapi', '0002_loanapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='last_emi_payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('late_payment', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='loanapi.loanapplication')),
            ],
        ),
        migrations.CreateModel(
            name='EMI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_emi_date', models.DateField(blank=True, null=True)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loanapi.loanapplication')),
            ],
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-29 19:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('annual_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('credit_score', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]

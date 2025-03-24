# Generated by Django 5.1.7 on 2025-03-23 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flights", "0002_flight_source_alter_flight_arrival_airport_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airline",
            name="iata_code",
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="airline",
            name="icao_code",
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="airline",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]

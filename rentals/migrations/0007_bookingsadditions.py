# Generated by Django 5.1.6 on 2025-02-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0006_alter_bookings_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingsAdditions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'bookings_additions',
                'managed': False,
            },
        ),
    ]

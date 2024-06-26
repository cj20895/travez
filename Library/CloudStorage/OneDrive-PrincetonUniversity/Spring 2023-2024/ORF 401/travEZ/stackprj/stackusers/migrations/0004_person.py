# Generated by Django 4.2.9 on 2024-04-29 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackusers', '0003_alter_profile_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(default='', max_length=64)),
                ('origination', models.CharField(max_length=64)),
                ('origination_state', models.CharField(default='', max_length=2)),
                ('destination_city', models.CharField(max_length=64)),
                ('destination_state', models.CharField(max_length=2)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('taking_passengers', models.BooleanField(default=False)),
                ('pet_friendly', models.BooleanField(default=False)),
                ('accessible', models.BooleanField(default=False)),
                ('seats_available', models.IntegerField(default='')),
                ('vehicle_type', models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Minivan', 'Minivan'), ('Van', 'Van'), ('Truck', 'Truck'), ('Other', 'Other')], default='Sedan', max_length=20)),
            ],
        ),
    ]

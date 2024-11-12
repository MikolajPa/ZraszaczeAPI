# Generated by Django 5.1.2 on 2024-10-13 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zraszacze_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('GUID', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day_of_week', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zraszacze_api.device')),
            ],
        ),
    ]

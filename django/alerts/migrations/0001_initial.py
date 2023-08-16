# Generated by Django 4.1.5 on 2023-08-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alerts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.CharField(max_length=128)),
                ('expr', models.CharField(max_length=128)),
                ('duration', models.CharField(max_length=8)),
                ('severity', models.IntegerField(choices=[(0, 'unknown'), (1, 'warning'), (2, 'critical')])),
                ('summary', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
    ]

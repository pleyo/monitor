# Generated by Django 4.1.5 on 2023-07-25 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0002_alter_metrics_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='lighthouse',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='server',
            name='prometheus',
            field=models.BooleanField(default=False),
        ),
    ]

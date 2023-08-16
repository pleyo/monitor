# Generated by Django 4.1.5 on 2023-08-16 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('alerts', '0002_alter_alerts_options_remove_alerts_alert_alerts_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerts',
            name='critical_duration',
            field=models.CharField(default='5m', max_length=8),
        ),
        migrations.AddField(
            model_name='alerts',
            name='warning_duration',
            field=models.CharField(default='2m', max_length=8),
        ),
        migrations.AlterUniqueTogether(
            name='alerts',
            unique_together={('name', 'severity')},
        ),
        migrations.CreateModel(
            name='DisableAlerts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disablealert', to='alerts.alerts')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disablealerts', to='projects.project')),
            ],
            options={
                'verbose_name': 'Disable Alert',
                'verbose_name_plural': 'Disable Alerts',
            },
        ),
        migrations.RemoveField(
            model_name='alerts',
            name='duration',
        ),
    ]

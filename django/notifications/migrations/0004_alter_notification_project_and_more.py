# Generated by Django 4.1.5 on 2023-09-05 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('availability', '0001_initial'),
        ('notifications', '0003_alter_notification_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='availability.service'),
        ),
    ]

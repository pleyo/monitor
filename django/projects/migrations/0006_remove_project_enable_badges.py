# Generated by Django 4.1.5 on 2023-01-11 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_enable_badges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='enable_badges',
        ),
    ]

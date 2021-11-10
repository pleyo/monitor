# Generated by Django 3.2.7 on 2021-11-10 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('is_public', models.BooleanField(default=True, help_text='Service will appears on application status board', verbose_name='Is visible')),
                ('is_enabled', models.BooleanField(default=True, help_text='Disabled service will not be monitored')),
                ('is_critical', models.BooleanField(default=True, help_text='Application is offline if this service fail, otherwise will only report as degraded')),
                ('creation_date', models.DateTimeField(auto_now_add=True, help_text='Creation date')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='HTTPMockedCodeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(choices=[(200, '200 - OK'), (404, '404 - Not Found'), (418, '418 - I’m a teapot'), (500, '500 - Internal Server Error')])),
                ('service', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='httpmockedcode', to='projects.service')),
            ],
        ),
        migrations.CreateModel(
            name='HTTPCodeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=512)),
                ('service', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='httpcode', to='projects.service')),
            ],
        ),
    ]

# Generated by Django 4.1.5 on 2023-08-16 09:56

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
                ('is_favorite', models.BooleanField(default=False, help_text='Favorite project are highlighted and first shown when possible.', verbose_name='Is favorite')),
                ('enable_public_page', models.BooleanField(default=False, help_text='Will enable the public page to share current project status', verbose_name='Enable public page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

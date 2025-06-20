# Generated by Django 5.2 on 2025-06-20 19:18

import django.contrib.postgres.indexes
import django.contrib.postgres.search
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_coldemail_resume_delete_task_coldemail_resume'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('resume_file_name', models.CharField(max_length=255)),
                ('resume_content', models.TextField()),
                ('target_company', models.CharField(max_length=255)),
                ('role_applied_for', models.CharField(max_length=255)),
                ('tone', models.CharField(choices=[('formal', 'Formal'), ('friendly', 'Friendly'), ('bold', 'Bold')], max_length=20)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'History Entries',
                'ordering': ['-created_at'],
                'indexes': [django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='api_history_search__2a131d_gin')],
            },
        ),
    ]

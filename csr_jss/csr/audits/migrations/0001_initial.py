# Generated by Django 3.1.3 on 2021-04-05 09:21

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
            name='AuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=200)),
                ('project', models.CharField(blank=True, max_length=500, null=True)),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('previous_state', models.TextField(blank=True)),
                ('current_state', models.TextField(blank=True)),
                ('reason', models.CharField(max_length=2048, null=True)),
                ('ip', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auditlog',
            },
        ),
    ]

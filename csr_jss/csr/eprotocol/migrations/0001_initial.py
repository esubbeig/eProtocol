# Generated by Django 3.1.3 on 2021-04-05 09:21

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='eProtocolHelp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec_heading', models.TextField()),
                ('sec_content', ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'eProtocolHelp',
            },
        ),
        migrations.CreateModel(
            name='eProtocolProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=254)),
                ('name', models.CharField(max_length=1024)),
                ('short_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('upin', models.CharField(blank=True, max_length=30, null=True)),
                ('nct', models.CharField(blank=True, max_length=254, null=True)),
                ('study_type', models.CharField(blank=True, max_length=100, null=True)),
                ('funding_entity', models.TextField(blank=True, null=True)),
                ('ind_sponsor', models.CharField(blank=True, max_length=1024, null=True)),
                ('sub_speciality', models.CharField(max_length=1024)),
                ('archived', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='eProtocolTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, error_messages={'unique': 'This code is already existed.'}, max_length=254, null=True, unique=True)),
                ('version_no', models.CharField(max_length=10)),
                ('delete', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('has_data', models.BooleanField(blank=True, default=False, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('therapeutic_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.therapeuticarea')),
            ],
            options={
                'db_table': 'eProtocolTemplate',
            },
        ),
        migrations.CreateModel(
            name='eProtocolTemplateSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec_heading', models.TextField()),
                ('sec_content', models.TextField(blank=True, null=True)),
                ('read_only', models.CharField(blank=True, max_length=10, null=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprotocol.eprotocoltemplate')),
            ],
            options={
                'db_table': 'eProtocolTemplateSections',
            },
        ),
        migrations.CreateModel(
            name='eProtocolProjectXUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eprotocolprojectxusers_created_by', to=settings.AUTH_USER_MODEL)),
                ('eProtocolproject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprotocol.eprotocolprojectinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'eProtocolProjectXUsers',
            },
        ),
        migrations.CreateModel(
            name='eProtocolProjectSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec_heading', models.TextField()),
                ('sec_content', models.TextField()),
                ('read_only', models.CharField(blank=True, max_length=10, null=True)),
                ('eProtocolproject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprotocol.eprotocolprojectinfo')),
            ],
            options={
                'db_table': 'eProtocolProjectSections',
            },
        ),
        migrations.AddField(
            model_name='eprotocolprojectinfo',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprotocol.eprotocoltemplate'),
        ),
        migrations.AddField(
            model_name='eprotocolprojectinfo',
            name='therapeutic_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.therapeuticarea'),
        ),
    ]

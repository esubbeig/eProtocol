# Generated by Django 3.1.3 on 2021-05-02 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eprotocol', '0002_auto_20210406_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefecenceCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_count', models.PositiveIntegerField(default=0)),
                ('eProtocolproject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprotocol.eprotocolprojectinfo')),
            ],
            options={
                'db_table': 'RefecenceCount',
            },
        ),
    ]

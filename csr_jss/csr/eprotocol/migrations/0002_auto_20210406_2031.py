# Generated by Django 3.1.3 on 2021-04-06 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eprotocol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eprotocoltemplate',
            name='code',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]

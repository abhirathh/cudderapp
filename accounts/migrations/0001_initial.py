# Generated by Django 4.0.4 on 2022-11-19 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userApiConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=0, max_length=255)),
                ('api_key', models.CharField(default=0, max_length=255)),
                ('secret_key', models.CharField(default=0, max_length=255)),
                ('timestamp', models.CharField(default=0, max_length=255)),
            ],
        ),
    ]

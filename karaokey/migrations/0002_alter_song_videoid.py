# Generated by Django 4.0.5 on 2022-10-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaokey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='videoId',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]

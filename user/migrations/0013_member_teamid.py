# Generated by Django 2.0.5 on 2018-05-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='teamid',
            field=models.CharField(default='NA', max_length=7),
        ),
    ]

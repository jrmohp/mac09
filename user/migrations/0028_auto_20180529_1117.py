# Generated by Django 2.0.5 on 2018-05-29 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_auto_20180529_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamdata',
            name='carnumber',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 2.0.4 on 2018-04-29 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20180429_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamdata',
            name='otp',
            field=models.IntegerField(max_length=8, null=True),
        ),
    ]

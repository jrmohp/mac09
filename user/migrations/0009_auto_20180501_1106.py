# Generated by Django 2.0.4 on 2018-05-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20180501_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamdata',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]

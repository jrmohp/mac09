# Generated by Django 2.0.4 on 2018-05-01 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20180501_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamdata',
            name='email',
        ),
    ]

# Generated by Django 2.1.11 on 2021-04-03 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0053_teamdata_vtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamdata',
            name='rsvp',
            field=models.BooleanField(default=False),
        ),
    ]

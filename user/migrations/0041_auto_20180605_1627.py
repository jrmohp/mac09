# Generated by Django 2.0.5 on 2018-06-05 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_member_memberid'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='idproof',
            field=models.ImageField(default='regback..png', upload_to=''),
        ),
        migrations.AddField(
            model_name='faculty',
            name='profilepic',
            field=models.ImageField(default='members/male.png', upload_to='members/'),
        ),
    ]

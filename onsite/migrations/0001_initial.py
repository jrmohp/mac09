# Generated by Django 4.0 on 2024-05-09 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0055_auto_20210407_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annexure1', models.BooleanField(default=False)),
                ('annexure2', models.BooleanField(default=False)),
                ('annexure3', models.BooleanField(default=False)),
                ('faculty_accompanied', models.BooleanField(default=False)),
                ('team_members_present', models.IntegerField(default=0)),
                ('check_in_time', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.teamdata')),
            ],
        ),
    ]

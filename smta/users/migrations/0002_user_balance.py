# Generated by Django 2.0.6 on 2018-06-16 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-10 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20200910_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='artist',
        ),
        migrations.AddField(
            model_name='track',
            name='artists',
            field=models.ManyToManyField(to='database.Artist'),
        ),
    ]

# Generated by Django 3.2.5 on 2021-07-12 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FuturePlanning', '0009_auto_20210712_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='End_Date',
            field=models.CharField(default='mm_yyyy', max_length=20),
        ),
        migrations.AddField(
            model_name='records',
            name='Value',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

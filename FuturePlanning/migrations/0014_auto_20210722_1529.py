# Generated by Django 3.2.5 on 2021-07-22 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FuturePlanning', '0013_c_events_c_familys_c_records'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='c_events',
            name='Fam_name',
        ),
        migrations.RemoveField(
            model_name='c_records',
            name='Fam_name',
        ),
        migrations.AddField(
            model_name='c_events',
            name='Family',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FuturePlanning.c_familys'),
        ),
        migrations.AddField(
            model_name='c_records',
            name='Family',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FuturePlanning.c_familys'),
        ),
    ]
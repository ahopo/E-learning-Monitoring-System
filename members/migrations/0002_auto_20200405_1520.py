# Generated by Django 2.1.5 on 2020-04-05 07:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compliantcourse',
            name='employee',
        ),
        migrations.AddField(
            model_name='compliantcourse',
            name='employee_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compliantcourse',
            name='employee_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]

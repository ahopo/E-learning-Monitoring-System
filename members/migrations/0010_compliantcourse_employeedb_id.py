# Generated by Django 3.0.5 on 2020-04-11 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_compliantcourse_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='compliantcourse',
            name='employeedb_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

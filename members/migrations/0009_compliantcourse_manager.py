# Generated by Django 3.0.5 on 2020-04-11 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_course_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='compliantcourse',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.Manager', verbose_name='MANAGER'),
        ),
    ]
# Generated by Django 2.1.5 on 2020-04-05 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20200405_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compliantcourse',
            name='status',
            field=models.CharField(choices=[('1', 'Compliant'), ('2', 'Non compliant')], default='2', max_length=20),
        ),
    ]
# Generated by Django 4.1.2 on 2022-10-27 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0004_alter_dailyreport_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='day',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='تاريخ اليوم'),
        ),
    ]

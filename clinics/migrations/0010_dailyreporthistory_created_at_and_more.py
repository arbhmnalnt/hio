# Generated by Django 4.0.6 on 2022-11-17 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0009_alter_dailyreport_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreporthistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='dailyreporthistory',
            name='created_at_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='dailyreporthistory',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dailyreporthistory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='dailyreporthistory',
            name='updated_at_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]

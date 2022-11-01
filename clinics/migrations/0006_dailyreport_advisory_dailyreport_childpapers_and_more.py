# Generated by Django 4.0.6 on 2022-10-31 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0005_alter_dailyreport_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreport',
            name='advisory',
            field=models.IntegerField(default=0, verbose_name='حالات الاستشارى'),
        ),
        migrations.AddField(
            model_name='dailyreport',
            name='childPapers',
            field=models.IntegerField(default=0, verbose_name='إجمالى روشتات الاطفال'),
        ),
        migrations.AddField(
            model_name='dailyreport',
            name='papers',
            field=models.IntegerField(default=0, verbose_name='إجمالى الروشتات'),
        ),
        migrations.AddField(
            model_name='dailyreport',
            name='specialist',
            field=models.IntegerField(default=0, verbose_name='حالات الاخصائى'),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='num',
            field=models.IntegerField(default=0, verbose_name='الإجمالى'),
        ),
    ]

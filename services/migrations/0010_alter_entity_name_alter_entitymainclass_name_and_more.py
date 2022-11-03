# Generated by Django 4.0.6 on 2022-10-28 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_entitymainclass_entitysubclass_servicemainclass_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='name',
            field=models.CharField(db_index=True, default='-', max_length=100),
        ),
        migrations.AlterField(
            model_name='entitymainclass',
            name='name',
            field=models.CharField(db_index=True, default='-', max_length=100, verbose_name='التصنيف الرئيسى'),
        ),
        migrations.AlterField(
            model_name='entitysubclass',
            name='name',
            field=models.CharField(db_index=True, default='-', max_length=100, verbose_name='التصنيف الرئيسى'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='naId',
            field=models.CharField(db_index=True, max_length=14, verbose_name='الرقم القومى'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='اسم المريض ثلاثى'),
        ),
        migrations.AlterField(
            model_name='service',
            name='code',
            field=models.IntegerField(db_index=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(db_index=True, default='-', max_length=100, verbose_name='اسم الخدمة'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='servicemainclass',
            name='name',
            field=models.CharField(db_index=True, default='-', max_length=100, verbose_name='التصنيف الرئيسى'),
        ),
        migrations.AlterField(
            model_name='servicesubclass',
            name='name',
            field=models.CharField(db_index=True, default='-', max_length=100, verbose_name='التصنيف الرئيسى'),
        ),
    ]
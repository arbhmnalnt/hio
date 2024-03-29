# Generated by Django 4.1.2 on 2022-10-26 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_rename_ayada_employee_area'),
        ('clinics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('ayada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_ayada', to='services.ayadat', verbose_name='العيادة')),
                ('specific', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinics.specific', verbose_name='العيادة')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('day', models.DateField(auto_now_add=True, null=True, verbose_name='التاريخ')),
                ('num', models.IntegerField(verbose_name='عدد المترددين')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinics.category', verbose_name='العيادة')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

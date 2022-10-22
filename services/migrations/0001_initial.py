# Generated by Django 4.1.2 on 2022-10-22 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(default='-', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ayadat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(default='تجربة', max_length=50)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ayada_area', to='services.area')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(default='-', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Law',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(default='-', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(default='-', max_length=100, verbose_name='اسم الخدمة')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_at_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(default='تجربة', max_length=50)),
                ('naId', models.CharField(default='2980504252201', max_length=14)),
                ('by_doctor', models.CharField(default='تجربة', max_length=50)),
                ('diagnosis', models.CharField(default='تجربة', max_length=50, verbose_name='التشخيص')),
                ('description', models.CharField(default='تجربة', max_length=50, verbose_name='وصف الحالة')),
                ('created_by', models.CharField(blank=True, default='تجربة', max_length=50, null=True)),
                ('ayada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letter_law', to='services.ayadat')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letter_entity', to='services.entity')),
                ('law', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letter_law', to='services.law')),
                ('services', models.ManyToManyField(blank=True, null=True, related_name='letters', to='services.service', verbose_name='الخدمات')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

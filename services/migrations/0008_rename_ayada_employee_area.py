# Generated by Django 4.1.2 on 2022-10-26 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_rename_area_employee_ayada'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='ayada',
            new_name='area',
        ),
    ]

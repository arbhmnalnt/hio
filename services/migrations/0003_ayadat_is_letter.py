# Generated by Django 4.0.6 on 2022-10-25 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_entity_address_entity_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='ayadat',
            name='is_letter',
            field=models.BooleanField(default=True),
        ),
    ]
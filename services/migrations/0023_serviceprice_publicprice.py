# Generated by Django 4.0.6 on 2023-01-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0022_serviceprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprice',
            name='publicPrice',
            field=models.IntegerField(default=0, verbose_name='توريد المنتفع'),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-28 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcard',
            name='card_number',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 3.1 on 2020-08-15 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='back',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='card',
            name='front',
            field=models.TextField(max_length=500),
        ),
    ]
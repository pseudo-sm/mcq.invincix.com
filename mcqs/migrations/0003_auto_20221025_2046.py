# Generated by Django 3.1.5 on 2022-10-25 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcqs', '0002_auto_20221025_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='registration_no',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

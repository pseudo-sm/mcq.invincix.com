# Generated by Django 3.2.16 on 2022-10-30 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcqs', '0008_alter_submission_choice_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='create_date_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
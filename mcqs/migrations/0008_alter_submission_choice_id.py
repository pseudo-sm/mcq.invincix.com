# Generated by Django 3.2.16 on 2022-10-30 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mcqs', '0007_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='choice_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mcqs.option'),
        ),
    ]

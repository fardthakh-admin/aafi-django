# Generated by Django 4.2.5 on 2023-09-24 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_alter_question_correct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='correct',
            new_name='correct_answer',
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-09 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0023_rename_actions_cbt_behavior_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="goal",
            old_name="name",
            new_name="goalName",
        ),
    ]

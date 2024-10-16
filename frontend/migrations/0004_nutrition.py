# Generated by Django 5.0.6 on 2024-06-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_majorassessment_alter_items_data_remove_items_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='nutrition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carbContent', models.CharField(default=None, max_length=100)),
                ('name_ar', models.CharField(default=None, max_length=100)),
                ('name_en', models.CharField(default=None, max_length=100)),
                ('portion', models.CharField(default=None, max_length=100)),
                ('proteinContent', models.CharField(default=None, max_length=100)),
                ('totalCalories', models.IntegerField(default=None, max_length=100)),
                ('weight', models.IntegerField(default=None, max_length=100)),
            ],
        ),
    ]

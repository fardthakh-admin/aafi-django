# Generated by Django 5.0.6 on 2024-05-14 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_item_remove_items_data_categories_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='majorAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default=None, max_length=100)),
                ('numberOfQuestions', models.IntegerField()),
                ('order', models.IntegerField()),
                ('title', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='items',
            name='data',
            field=models.CharField(max_length=255),
        ),
        migrations.RemoveField(
            model_name='items',
            name='name',
        ),
        migrations.AddField(
            model_name='items',
            name='categories',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='assessmentQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max', models.IntegerField(default=0)),
                ('order', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('question', models.CharField(max_length=100)),
                ('majorAssessment', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='frontend.majorassessment')),
            ],
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]

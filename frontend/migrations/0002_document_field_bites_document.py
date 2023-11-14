# Generated by Django 4.2.5 on 2023-11-13 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('difficulty', models.IntegerField()),
                ('tags', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.document')),
            ],
        ),
        migrations.AddField(
            model_name='bites',
            name='document',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='frontend.document'),
            preserve_default=False,
        ),
    ]

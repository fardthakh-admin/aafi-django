# Generated by Django 4.2.5 on 2024-01-12 22:40

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=60, null=True, unique=True)),
                ('role', models.CharField(choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')], default='Patient', max_length=10)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('length', models.IntegerField(null=True)),
                ('time', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('deadLine', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feetSituation', models.CharField(choices=[('cuts', 'cuts'), ('redness', 'redness'), ('swelling', 'swelling'), ('sores', 'sores'), ('blisters', 'blisters'), ('corns', 'corns'), ('calluses', 'calluses'), ('change_to_the_skin_or_nails', 'change to the skin or nails')], max_length=100, null=True)),
                ('FBS', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('mood', models.CharField(choices=[('1', "I'm feeling great"), ('2', "I'm feeling good"), ('3', "I'm feeling ok"), ('4', "I'm feeling bad"), ('5', "I'm feeling awful")], max_length=50, null=True)),
                ('sleepHours', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250, null=True)),
                ('option1', models.CharField(max_length=250, null=True)),
                ('option2', models.CharField(max_length=250, null=True)),
                ('option3', models.CharField(max_length=250, null=True)),
                ('category', models.CharField(max_length=250, null=True)),
                ('points', models.IntegerField(null=True)),
                ('correct_answer', models.CharField(max_length=250, null=True)),
                ('incorrect_answers', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Doctor',
            },
            bases=('api.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('patientRole', models.CharField(choices=[('Patient', 'Patient'), ('Sponsor', 'Sponsor')], default='Patient', max_length=20)),
                ('my_doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.doctor')),
            ],
            options={
                'verbose_name': 'Patient',
            },
            bases=('api.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(choices=[('once_a_day', 'once a day'), ('twice_a_day', 'twice a day')], max_length=50, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalDiagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosisName', models.CharField(blank=True, max_length=150, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('diagnosisDate', models.DateField(blank=True, null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.CharField(max_length=100, null=True)),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('patients', models.ManyToManyField(related_name='our_group', to='api.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goalName', models.CharField(max_length=100, null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('achievement', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.activity')),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.badge')),
                ('challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.challenge')),
                ('checkIn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.checkin')),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.game')),
                ('goal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.goal')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
        migrations.AddField(
            model_name='checkin',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patient'),
        ),
        migrations.CreateModel(
            name='CBT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thought', models.TextField()),
                ('feeling', models.TextField()),
                ('behavior', models.TextField()),
                ('date', models.DateField(null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Biomarkers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fbs', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('hba1c', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('bmi', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('date', models.DateField(null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='patients',
            field=models.ManyToManyField(related_name='activities', to='api.patient'),
        ),
    ]

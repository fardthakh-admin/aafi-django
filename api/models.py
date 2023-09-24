from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class ModelManager(models.Manager):
    pass


class BaseModel(models.Model):
    objects = ModelManager()

    class Meta:
        abstract = True


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
    )

    username = models.CharField(unique=True, max_length=60, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Patient')

    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    phone_number = models.CharField(max_length=17, null=True, blank=True)  # Needs validator

    REQUIRED_FIELDS = []

    def is_patient(self):
        return self.role == 'Patient'

    def is_Doctor(self):
        return self.role == 'Doctor'

    def __str__(self):
        return self.username


class Doctor(User):
    def save(self, *args, **kwargs):
        self.role = 'Doctor'
        super(Doctor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Doctor'

    def __str__(self):
        return self.username


class Patient(User):
    DOB = models.DateField(null=True, blank=True)
    my_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

    PATIENT_ROLE_CHOICES = (
        ('Patient', 'Patient'),
        ('Sponsor', 'Sponsor'),
    )
    patientRole = models.CharField(max_length=20, choices=PATIENT_ROLE_CHOICES, default='Patient')

    def is_sponsor(self):
        return self.patientRole == 'Sponsor'

    def save(self, *args, **kwargs):
        self.role = 'Patient'
        super(Patient, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Patient'

    def __str__(self):
        return self.username


class Medication(models.Model):
    frequency_choices = [
        ('once_a_day', 'once a day'),
        ('twice_a_day', 'twice a day'),
    ]
    frequency = models.CharField(max_length=50, null=True, choices=frequency_choices)
    name = models.CharField(max_length=100, null=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=100, null=True)
    length = models.IntegerField(null=True)
    time = models.TimeField(null=True)

    patients = models.ManyToManyField('Patient', related_name='activities')  # many-to-many relation

    def __str__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(max_length=100, null=True)
    deadLine = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return self.body[0:50]


class Groups(models.Model):
    groupName = models.CharField(max_length=100, null=True)
    dateCreated = models.DateField(auto_now_add=True)

    patients = models.ManyToManyField('Patient', related_name='our_group')  # many-to-many relation

    def __str__(self):
        return self.groupName


# check datatypes
class CheckIn(models.Model):
    MOOD_CHOICES = [
        ("1", "I'm feeling great"),
        ("2", "I'm feeling good"),
        ("3", "I'm feeling ok"),
        ("4", "I'm feeling bad"),
        ("5", "I'm feeling awful"),
    ]

    FEET_SITUATION_CHOICES = [
        ('cuts', 'cuts'),
        ('redness', 'redness'),
        ('swelling', 'swelling'),
        ('sores', 'sores'),
        ('blisters', 'blisters'),
        ('corns', 'corns'),
        ('calluses', 'calluses'),
        ('change_to_the_skin_or_nails', 'change to the skin or nails'),
    ]
    feetSituation = models.CharField(max_length=100, choices=FEET_SITUATION_CHOICES, null=True)  # key value
    FBS = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES, null=True)
    sleepHours = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.FBS


class Biomarkers(models.Model):
    fbs = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    hba1c = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    date = models.DateField(null=True)

    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.date


class Goal(models.Model):
    goalName = models.CharField(max_length=100, null=True)
    end_time = models.DateTimeField(null=True)
    achievement = models.TextField(null=True)
    image = models.ImageField(null=True)

    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.goalName


class Badge(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True)  # default

    def __str__(self):
        return self.name


class CBT(models.Model):
    thought = models.TextField()
    feeling = models.TextField()
    behavior = models.TextField()
    date = models.DateField(null=True)

    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.date


class Game(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=250, null=True)
    option1 = models.CharField(max_length=250, null=True)
    option2 = models.CharField(max_length=250, null=True)
    option3 = models.CharField(max_length=250, null=True)
    category = models.CharField(max_length=250, null=True)

    points = models.IntegerField(null=True)
    correct_answer = models.CharField(max_length=250, null=True)
    incorrect_answers = models.CharField(max_length=250, null=True)


    def __str__(self):
        return self.question


class Evaluation(models.Model):
    points = models.IntegerField()

    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, null=True, blank=True, on_delete=models.CASCADE)
    checkIn = models.ForeignKey(CheckIn, null=True, blank=True, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, null=True, blank=True, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.points


class HistoricalDiagnosis(models.Model):
    diagnosisName = models.CharField(max_length=150, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    diagnosisDate = models.DateField(null=True, blank=True)

    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.diagnosisName


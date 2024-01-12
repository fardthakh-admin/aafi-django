from django import forms
from django.forms import ModelForm
from api.models import Doctor, Patient
from .models import *


class PatientForm(ModelForm):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]

    gender = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=GENDER_CHOICES,
    )

    class Meta:
        model = Patient
        fields = ('username', 'email', 'password', 'address', 'gender', 'phone_number', 'DOB')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),  # email needs validator
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),  # phone also needs validators
            'DOB': forms.DateInput(attrs={'type': 'date'}),
        }


class DoctorForm(ModelForm):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]

    gender = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=GENDER_CHOICES,
    )

    class Meta:
        model = Doctor
        fields = ('username', 'email', 'password', 'address', 'gender', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

    def __init__(self, *args, **kwargs):
        self.consultant = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # doctor status is set to False by default
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


    
class DocumentForm(forms.Form):
    patient_id = forms.CharField(label='Patient ID', max_length=100)
    title = forms.CharField(label='Title', max_length=100)

    TAG_CHOICES = [
        ('tag1', ' Title'),
        ('tag2', ' description '),
    ]

    tags = forms.ChoiceField(label='Tags', choices=TAG_CHOICES)
    content = forms.CharField(label='Content', max_length=100)
    difficulty = forms.CharField(label='Difficulty', max_length=100)
    category = forms.CharField(label='Category', max_length=100)



class TagsForm(forms.ModelForm):
      class Meta:
        model = tags
        fields = "__all__"


class ActivitiesForm(forms.ModelForm):
     class Meta:
        model=activities
        fields = "__all__"

class AssessmentQuestionForm(forms.ModelForm):
    # Get a list of tuples for majorAssessment choices
    MAJOR_ASSESSMENT_CHOICES = [(obj.id, obj.title) for obj in majorAssessment.objects.all()]

    majorAssessment = forms.ChoiceField(choices=MAJOR_ASSESSMENT_CHOICES, label='Major Assessment')

    class Meta:
        model = assessmentQuestion
        fields = ['majorAssessment', 'max', 'order', 'points', 'question']


class BadgesForm(forms.ModelForm):
     class Meta:
        model=badges
        fields = "__all__"


class BiomarkersForm(forms.ModelForm):
      class Meta:
        model=biomarkers
        fields = "__all__"


class CategoriesForm(forms.ModelForm):
     class Meta:
        model=categories
        fields = "__all__"



class FeelingsForm(forms.ModelForm):
     class Meta:
        model=feelings
        fields = "__all__"

class InAppLinksForm(forms.ModelForm):
     class Meta:
        model=inAppLinks
        fields = "__all__"

class InquiryForm(forms.ModelForm):
     class Meta:
        model=inquiry
        fields = "__all__"



class ItemForm(forms.ModelForm):
    class Meta:
        model = items
        fields = ['name', 'data_title', 'data_categories']

class JournalForm(forms.ModelForm):
     class Meta:
        model=journal
        fields = "__all__"


class JournalPromptForm(forms.ModelForm):
     class Meta:
        model=journalPrompt
        fields = "__all__"


class MajorAssessmentForm(forms.ModelForm):
     class Meta:
        model=majorAssessment
        fields = "__all__"

class PsychomarkersForm(forms.ModelForm):
     class Meta:
        model=psychomarkers
        fields = "__all__"

class ScenariosForm(forms.ModelForm):
     class Meta:
        model=scenarios
        fields = "__all__"


class ShortBiteForm(forms.ModelForm):
     class Meta:
        model=shortBite
        fields = "__all__"


class TriviaForm(forms.ModelForm):
     class Meta:
        model=trivia
        fields = "__all__"


class UsersForm(forms.ModelForm):
     class Meta:
        model=users
        fields = "__all__"

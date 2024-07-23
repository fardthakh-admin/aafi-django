from django import forms
from django.forms import ModelForm
from api.models import Doctor, Patient
from .models import *
from django.forms import Textarea



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
        # fields = "__all__"
        exclude = ['image']


class ActivitiesForm(forms.ModelForm):
     class Meta:
        model=activities
        fields =  "__all__"


class AssetsForm(forms.ModelForm):
     class Meta:
        model=assets
        fields = "__all__"

class SelfAwarenessScenariosForm(forms.ModelForm):
     class Meta:
        model=selfAwarenessScenarios
        fields = "__all__"

class SelfLadderForm(forms.ModelForm):
     class Meta:
        model=selfLadder
        fields = "__all__"

class selfAwarnessBitesForm(forms.ModelForm):
     class Meta:
        model=selfAwarnessBites
        fields = "__all__"        

class wildCardForm(forms.ModelForm):
     class Meta:
        model=wildCard
        fields = "__all__"        


class BadgesForm(forms.ModelForm):
     class Meta:
        model=badges
        fields = "__all__"


class BiomarkersForm(forms.ModelForm):
      class Meta:
        model=biomarkers
        exclude = ['user']  # all without user



class CategoriesForm(forms.ModelForm):
     class Meta:
        model=categories
        fields = "__all__"



class FeelingsForm(forms.ModelForm):
     class Meta:
        model=feelings
        exclude = ['user', 'time']

class InAppLinksForm(forms.ModelForm):
     class Meta:
        model=inAppLinks
        fields = "__all__"

class InquiryForm(forms.ModelForm):
     class Meta:
        model=inquiry
        exclude = ['time', 'user']

class MajorAssessmentForm(forms.ModelForm):
     class Meta:
        model=majorAssessment
        fields = "__all__"

class AssessmentQuestionForm(forms.ModelForm):
      class Meta:
        model=assessmentQuestion
        fields =['max', 'order', 'points', 'question']

class ItemsForm(forms.ModelForm):
      class Meta:
        model=items
        fields ="__all__"


# # class ItemsForm(forms.ModelForm):
# #     class Meta:
# #         model = items
# # #         fields = ['name', 'data']

# #     title = forms.CharField(max_length=100, required=False)
# #     categories = forms.CharField(max_length=100, required=False)

#     def clean(self):
#         cleaned_data = super().clean()
#         title = cleaned_data.get('title')
#         categories = cleaned_data.get('categories')
        
#         if title is not None or categories is not None:
#             cleaned_data['data'] = {'title': title, 'categories': categories}
#         return cleaned_data


class JournalForm(forms.ModelForm):
     class Meta:
        model=journal
        fields = "__all__"


class JournalPromptForm(forms.ModelForm):
     class Meta:
        model=journalPrompt
        fields = "__all__"
        




class PsychomarkersForm(forms.ModelForm):
     class Meta:
        model=psychomarkers
        exclude = ['time', 'user']


class ScenariosForm(forms.ModelForm):
     class Meta:
        model=scenarios
        fields = "__all__"


class ShortBiteForm(forms.ModelForm):
     class Meta:
        model=shortBite
        fields = "__all__"

class BitesForm(forms.ModelForm):


    class Meta:
        model = bites
        exclude = ['tags']


class TriviaForm(forms.ModelForm):
     class Meta:
        model=trivia
        fields = "__all__"


class UsersForm(forms.ModelForm):
     class Meta:
        model=users
        fields = "__all__"

class NutritionForm(forms.ModelForm):
     class Meta:
        model=nutrition
        fields = "__all__"


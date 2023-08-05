from django import forms
from django.forms import ModelForm
from api.models import Doctor, Patient


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
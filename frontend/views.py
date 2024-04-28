from django.shortcuts import render
import firebase_admin
#simport pandas as pd
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from firebase import firebase
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from api.models import User
from django.contrib.auth import get_user_model
from frontend.models import bites
import logging
from .forms import DocumentForm
from .forms import *
from django.http import JsonResponse
from .models import collection
from .models import *
from datetime import datetime
from .models import tags

db = firestore.client()
firebase_app = firebase.FirebaseApplication('https://techcare-diabetes.firebaseio.com', None)


config = {
    'apiKey': 'AIzaSyDYH31LLGfe492t4xklzTeZrIy_Rs-Om3M',
    'authDomain': 'techcare-diabetes.firebaseapp.com',
    'projectId': 'techcare-diabetes',
    'storageBucket': 'techcare-diabetes.appspot.com',
    'messagingSenderId': '1086234468488',
    'appId': '1:1086234468488:web:d32c01a322df2e0e76ff3d',
    'measurementId': 'G-VWVCF3QKTZ'
}

def index(request):
    return render(request, 'frontend/index.html'),

def logout_page(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request, 'frontend/index.html'),

def logout_page(request):
    logout(request)
    return redirect('login')


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        if request.user.is_patient():
            return redirect('patient-homepage')
        else:
            return redirect('doctor-homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(username=username).first()
        except:
            messages.error(request, 'User does not exist')

        if request.user is not None and request.user.is_authenticated:
            messages.error(request, 'Your account is still pending approval.')
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_patient():
                    # Log in the patient and redirect to the patient homepage
                    login(request, user)
                    return redirect('patient-homepage')
                elif user.is_Doctor():
                    # Log in the doctor and redirect to the doctor if approved
                    login(request, user)
                    return redirect('doctor-homepage')
            else:
                # Display error message if authentication fails
                messages.error(request, 'Invalid username or password')

    context = {'page': page}
    return render(request, 'login_signup.html', context)

   # def trivia_template_view(request):
    
    #  return render(request, 'patient/trivia.html')



@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login')


def patient_signup(request):
    page = 'patientSignup'
    form = PatientForm()

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.instance.password = make_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

    context = {'page': page,
               'form': form, }
    return render(request, 'frontend/patient_signup.html', context)


def doctor_signup(request):
    page = 'doctorSignup'
    form = DoctorForm()

    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.instance.password = make_password(form.cleaned_data['password'])
            form.save(commit=False)
            form.save()
            messages.success(request, 'Your account has been created and is pending approval.')
            return redirect('login')
        else:
            messages.error(request, 'error occurred')

    context = {'page': page,
               'form': form, }
    return render(request, 'frontend/doctor_signup.html', context)


@login_required(login_url='/login')
def patient_homepage(request):
    return render(request, 'frontend/patient/patientHomepage.html')


@login_required(login_url='/login')
def doctor_homepage(request):
    return render(request, 'frontend/doctor/doctorHomepage.html')


@login_required(login_url='/login')
def calendar(request):
    return render(request, 'frontend/calendar.html')


@login_required(login_url='/login')
def patients_list(request):
    return render(request, 'frontend/doctor/patients.html')

@login_required(login_url='/login')
def doctor_chat_page(request):
    return render(request, 'frontend/doctor/doctor-chat.html')


    
@login_required(login_url='/login')
def mind_activities_view(request):
    return render(request,'frontend/patient/activities.html')

@login_required(login_url='/login')
def quiz_question_view(request):
    return render(request,'frontend/patient/quiz.html')





def bites_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("bites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = BitesForm()   
    db = firestore.client()
    collection = db.collection("tags")
    documents = collection.stream()
    tags_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    return render(request, 'frontend/techcare_data/bites_table.html', {'form': form, 'tags_data': tags_data ,'document_data': document_data})

def bitesdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("bites")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/bitesdocument.html', {'document_data': document_data})


def create_document(request):
    if request.method == 'POST':
        form = BitesForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'tags': request.POST.get('tags'),
                'difficulty': form.cleaned_data['difficulty'],
                'categories': form.cleaned_data['categories'],
                'content': form.cleaned_data['content'],
            }
            db.collection("bites").document().set(data)  
            messages.success(request, 'Successfully created Bites.')  
            return redirect('bites_view') 
        else:
            messages.error(request, 'Error creating Bites. Please check your input.')
            return redirect('bites_view') 



def get_all_collections(request):
    db = firestore.client()
    all_collections = [collection.id for collection in db.collections()]
    return {'collections': all_collections}

def handle_form_submission(request):
    try:
        if request.method == 'POST':
            selected_collection = request.POST.get('collection_dropdown')
            collection_views = {
                'bites': 'bites_view',
                'activities': 'activities_view',
                'badges': 'badges_view',
                'biomarkers': 'biomarkers_view',
                'assessmentQuestion': 'assessmentQuestion_view',
                'categories': 'categories_view',
                'feelings': 'feelings_view',
                'inAppLinks': 'inAppLinks_view',
                'inquiry': 'inquiry_view',
                'items': 'items_view',
                'journal': 'journal_view',
                'journalPrompt': 'journalPrompt_view',
                'majorAssessment': 'majorAssessment_view',
                'psychomarkers': 'psychomarkers_view',
                'scenarios': 'scenarios_view',
                'shortBite': 'shortBite_view',
                'tags': 'tags_view',
                'trivia': 'trivia_view',
                'users': 'users_view',

            }

            if selected_collection in collection_views:
                # If yes, redirect to the corresponding view
                return redirect(collection_views[selected_collection])

    except Exception as e:
        # Handle the exception or log the error
        print(f"An error occurred: {e}")

    # Handle other cases or render the page
    return render(request, 'frontend/techcare_data/collections.html')



def activities_view(request):
    db = firestore.Client()
    collection = db.collection("activities")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = ActivitiesForm()   
    db = firestore.client()
    collection = db.collection("tags")
    documents = collection.stream()
    tags_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    return render(request, 'frontend/techcare_data/activities_table.html', {'form': form, 'tags_data': tags_data ,'document_data': document_data})

def assets_view(request):
    db = firestore.Client()
    collection = db.collection("assets")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = ActivitiesForm()   
    db = firestore.client()
    collection = db.collection("tags")
    documents = collection.stream()
    tags_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    return render(request, 'frontend/techcare_data/activities_table.html', {'form': form, 'tags_data': tags_data ,'document_data': document_data})


def activitiesdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("activities")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/activitiesdocument.html', {'document_data': document_data})

def badges_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("badges")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = BadgesForm() 
    return render(request, 'frontend/techcare_data/badges_table.html', {'form': form, 'document_data': document_data})

def badgesdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("badges")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/badgesdocument.html', {'document_data': document_data})

def biomarkers_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("biomarkers")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    form = BiomarkersForm()   
    db = firestore.client()
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    return render(request, 'frontend/techcare_data/biomarkers_table.html', {'form': form, 'users_data': users_data ,'document_data': document_data})

def biomarkersdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("biomarkers")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/biomarkersdocument.html', {'document_data': document_data})


def assessmentQuestion_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("assessmentQuestion")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = AssessmentQuestionForm()
    collection2 = db.collection("majorAssessment")
    documents2 = collection2.stream()
    majorAssessment = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents2]
    return render(request, 'frontend/techcare_data/assessmentQuestion_table.html', {'form': form, 'majorAssessment': majorAssessment, 'document_data': document_data})

def assessmentQuestiondocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("assessmentQuestion")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/assessmentQuestiondocument.html', {'document_data': document_data})

def categories_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("categories")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = CategoriesForm()
    return render(request, 'frontend/techcare_data/categories_table.html', {'document_data': document_data, 'form': form})

def categoriesdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("categories")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/categoriesdocument.html', {'document_data': document_data})

def feelings_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("feelings")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = FeelingsForm()
    collection2 = db.collection("user")
    documents2 = collection2.stream()
    feelings = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents2]
    return render(request, 'frontend/techcare_data/feelings_table.html', {'form': form, 'feelings': feelings, 'document_data': document_data})

def feelingsdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("feelings")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/feelingsdocument.html', {'document_data': document_data})

def inAppLinks_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("inAppLinks")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = InAppLinksForm()
    return render(request, 'frontend/techcare_data/inAppLinks_table.html', {'document_data': document_data, 'form': form})

def inAppLinksdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("inAppLinks")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/inAppLinksdocument.html', {'document_data': document_data})

def inquiry_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("inquiry")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = InquiryForm()
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    return render(request, 'frontend/techcare_data/inquiry_table.html', {'document_data': document_data, 'form': form, 'users_data': users_data})

def inquirydocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("inquiry")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/inquirydocument.html', {'document_data': document_data})


def items_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("items")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = ItemsForm()
    return render(request, 'frontend/techcare_data/items_table.html', {'document_data': document_data, 'form': form})

def itemsdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("items")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/itemsdocument.html', {'document_data': document_data})

def journal_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("journal")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = JournalForm()
    return render(request, 'frontend/techcare_data/journal_table.html', {'document_data': document_data, 'form': form})

def journaldocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("journal")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/journaldocument.html', {'document_data': document_data})

def journalPrompt_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("journalPrompt")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = JournalForm()
    return render(request, 'frontend/techcare_data/journalPrompt_table.html', {'document_data': document_data, 'form': form})
    
def journalPromptdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("journalPrompt")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/journalPromptdocument.html', {'document_data': document_data})

def majorAssessment_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("majorAssessment")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = MajorAssessmentForm()
    return render(request, 'frontend/techcare_data/majorAssessment_table.html', {'document_data': document_data, 'form': form})

def majorAssessmentdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("majorAssessment")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/majorAssessmentdocument.html', {'document_data': document_data})



def psychomarkers_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("psychomarkers")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = PsychomarkersForm()
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    return render(request, 'frontend/techcare_data/psychomarkers_table.html',{'document_data': document_data, 'form': form, 'users_data': users_data} )

def psychomarkersdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("psychomarkers")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/psychomarkersdocument.html', {'document_data': document_data})

def scenarios_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("scenarios")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = ScenariosForm()
    return render(request, 'frontend/techcare_data/scenarios_table.html', {'document_data': document_data , 'form': form})

def scenariosdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("scenarios")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/scenariosdocument.html', {'document_data': document_data})




def shortBite_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("shortBite")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = ShortBiteForm()
    return render(request, 'frontend/techcare_data/shortBite_table.html', {'document_data': document_data, 'form': form})
    
def shortBitedocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("shortBite")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/shortBitedocument.html', {'document_data': document_data})

def tags_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("tags")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = TagsForm()
    return render(request, 'frontend/techcare_data/tags_table.html', {'document_data': document_data, 'form': form})

def tagsdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("tags")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/tagsdocument.html', {'document_data': document_data})


def trivia_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("trivia")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = TriviaForm()
    return render(request, 'frontend/techcare_data/trivia_table.html', {'document_data': document_data, 'form': form})

def triviadocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("trivia")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/triviadocument.html', {'document_data': document_data})


def users_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("users")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    form = UsersForm()
    return render(request, 'frontend/techcare_data/users_table.html', {'document_data': document_data, 'form': form})


def usersdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("users")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/usersdocument.html', {'document_data': document_data})




def sidebar(request):
    firestore_collections = get_firestore_collections()
    return render(request, 'sidebar.html', {'firestore_collections': firestore_collections}) 

def create_tags(request):
    if request.method == 'POST':
        form = TagsForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],   
            }
            db.collection("tags").document().set(data)  
            messages.success(request, 'Success Creating Tags.')
            return redirect('tags_view')
        else:
             messages.error(request, 'Error creating Tags. Please check your input.')
             return redirect('tags_view')

def create_activities(request):
    if request.method == 'POST':
        form = ActivitiesForm(request.POST)
        if form.is_valid():
            data = {
                'tags': request.POST.get('tags'),
                'description': form.cleaned_data['description'],
                'title': form.cleaned_data['title'],
                'duration': form.cleaned_data['duration'],
            }
            db = firestore.client()
            db.collection("activities").document().set(data)
            messages.success(request, 'Success Creating Activity.')
            return redirect('activities_view')
        else:
             messages.error(request, 'Error creating activity. Please check your input.')
             return redirect('activities_view')
        

def create_assessmentQuestion(request):
    if request.method == 'POST':
        form = AssessmentQuestionForm(request.POST)
        if form.is_valid():
            data = {
                'majorAssessment': request.POST.get('majorAssessment'),   
                'max': form.cleaned_data['max'],
                'order': form.cleaned_data['order'],  
                'points': form.cleaned_data['points'],  
                'question': form.cleaned_data['question'],  
            }
            db = firestore.client()
            db.collection("assessmentQuestion").document().set(data)
            messages.success(request, 'Successfully created Assessment Question.')  
            return redirect('assessmentQuestion_view') 
        else:
            messages.error(request, 'Error creating Assessment Question. Please check your input.')
            return redirect('assessmentQuestion_view') 





def create_badges(request):
       if request.method == 'POST':
         form = BadgesForm(request.POST)
         if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],   
            }
            db.collection("badges").document().set(data)  
            messages.success(request, 'Successfully created Badges View.')  
            return redirect('badges_view') 
         else:
            messages.error(request, 'Error creating Badges View. Please check your input.')
            return redirect('badges_view') 

def create_biomarkers(request):
    if request.method == 'POST':
        form = BiomarkersForm(request.POST)
        if form.is_valid():
            data = {
                'dailyActivity': form.cleaned_data['dailyActivity'],
                'dailyCarbs': form.cleaned_data['dailyCarbs'],
                'sleepQuality': form.cleaned_data['sleepQuality'],
                'time': form.cleaned_data['time'],
                'user_id': request.POST.get('user_id'),
                'weeklyActivity': form.cleaned_data['weeklyActivity'],
                'weight': form.cleaned_data['weight'],
                'FBS': form.cleaned_data['FBS'],
                'HBA1c': form.cleaned_data['HBA1c'],
                'bloodGlucose': form.cleaned_data['bloodGlucose'],
                'bloodGlucoseType': form.cleaned_data['bloodGlucoseType'],
            }
            db.collection("biomarkers").document().set(data)
            messages.success(request, 'Successfully created Biomarkers View.')  
            return redirect('biomarkers_view') 
        else:
            messages.error(request, 'Error creating Biomarkers View. Please check your input.')
            return redirect('biomarkers_view') 


   
def create_categories(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            data = {
                'description': form.cleaned_data['description'], 
                'title': form.cleaned_data['title'],   
            }
            db.collection("categories").document().set(data)  
            messages.success(request, 'Successfully created Categories.')
            return redirect('categories_view') 
        else:
            messages.error(request, 'Error creating Categories. Please check your input.')
            return redirect('categories_view') 

   
def create_feelings(request):
       if request.method == 'POST':
         form = FeelingsForm(request.POST)
         if form.is_valid():
            data = {
                'anger': form.cleaned_data['anger'], 
                'fear': form.cleaned_data['fear'], 
                'happiness': form.cleaned_data['happiness'], 
                'joy': form.cleaned_data['joy'],   
                'love': form.cleaned_data['love'], 
               'sadness': form.cleaned_data['sadness'], 
               'shame': form.cleaned_data['shame'], 
                'strength': form.cleaned_data['strength'],   
                # 'time': form.cleaned_data['time'], 

            }
            db.collection("feelings").document().set(data)  
            messages.success(request, 'Successfully created Feelings.')
            return redirect('feelings_view') 
         else:
            messages.error(request, 'Error creating Feelings. Please check your input.')
            return redirect('feelings_view') 

def create_inAppLinks(request):
    if request.method == 'POST':
        form = InAppLinksForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'order': form.cleaned_data['order'],
                'type': form.cleaned_data['type'],
                
            }
            db.collection("inAppLinks").document().set(data)
            messages.success(request, 'Successfully created inAppLinks.')  
            return redirect('inAppLinks_view') 
        else:
            messages.error(request, 'Error creating inAppLinks. Please check your input.')
            return redirect('inAppLinks_view')

        
    return render(request, 'frontend/techcare_data/create_inAppLinks.html', {'form': form})
from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model

def create_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():

            data = {
                'question': form.cleaned_data['question'],
                'answer': form.cleaned_data['answer'],
                'topic': form.cleaned_data['topic'],
                'user': request.POST.get('user_id'),
                'time': timezone.now(),
            }

            # Save the data to Firestore
            db.collection("inquiry").document().set(data)  

            messages.success(request, 'Successfully created Inquiry.') 
            return redirect('inquiry_view')
        else:
            messages.error(request, 'Error creating Inquiry. Please check your input.')
            return redirect('inquiry_view')



def create_journal(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
              
            }
            db.collection("journal").document().set(data)  
            messages.success(request, 'Successfully created Journal.') 
            return redirect('journal_view')
        else:
            messages.error(request, 'Error creating Journal. Please check your input.')
            return redirect('journal_view')


def create_journalPrompt(request):
    if request.method == 'POST':
        form = JournalPromptForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
              
            }
            db.collection("journalPrompt").document().set(data)  
            messages.success(request, 'Successfully created JournalPrompt.') 
            return redirect('journalPrompt_view')
        else:
            messages.error(request, 'Error creating JournalPrompt. Please check your input.')
            return redirect('journalPrompt_view')



def create_majorAssessment(request):
    if request.method == 'POST':
        form = MajorAssessmentForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'numberOfQuestions': form.cleaned_data['numberOfQuestions'],
                'description': form.cleaned_data['description'],
                'order': form.cleaned_data['order'],  # Removed the space before 'order'
            }
            db.collection("majorAssessment").document().set(data)  
            messages.success(request, 'Successfully created MajorAssessment.') 
            return redirect('majorAssessment_view')
        else:
            messages.error(request, 'Error creating MajorAssessment. Please check your input.')
            return redirect('majorAssessment_view')

def create_psychomarkers(request):
    if request.method == 'POST':
        form = PsychomarkersForm(request.POST)
        if form.is_valid():
            # user_id = form.cleaned_data['user'].id
            data = {
                'time': datetime.now(),
                'user': request.POST.get('user_id'),  # Assuming 'user' is a ForeignKey in your model, use the user_id
                'depression': form.cleaned_data['depression'],
            }
            db.collection("psychomarkers").document().set(data)
            messages.success(request, 'Successfully created Psychomarkers.') 
            return redirect('psychomarkers_view')
        else:
            messages.error(request, 'Error creating Psychomarkers. Please check your input.')
            return redirect('psychomarkers_view')

def create_scenarios(request):
    if request.method == 'POST':
        form = ScenariosForm(request.POST)
        if form.is_valid():
            data = {
                'PositiveCorrectionAlternative': form.cleaned_data['PositiveCorrectionAlternative'],
                'actionreply': form.cleaned_data['actionreply'],
                'correction': form.cleaned_data['correction'],
                'positiveActionReply': form.cleaned_data['positiveActionReply'],
                'title': form.cleaned_data['title'],
            }
            db.collection("scenarios").document().set(data)
            messages.success(request, 'Successfully created Scenarios.') 
            return redirect('scenarios_view')
        else:
            messages.error(request, 'Error creating Scenarios. Please check your input.')
            return redirect('scenarios_view')

    
def create_shortBite(request):
    if request.method == 'POST':
        form = ShortBiteForm(request.POST)
        if form.is_valid():
            data = {
                'order': form.cleaned_data['order'],
                'title': form.cleaned_data['title'],
            }
            db.collection("shortBite").document().set(data)
            messages.success(request, 'Successfully ShortBite Scenarios.') 
            return redirect('shortBite_view')
        else:
            messages.error(request, 'Error creating ShortBite. Please check your input.')
            return redirect('shortBite_view')


def create_trivia(request):
    if request.method == 'POST':
        form = TriviaForm(request.POST)
        if form.is_valid():
            data = {
                'CBT_points': form.cleaned_data['CBT_points'],
                'answer_1': form.cleaned_data['answer_1'],
                'answer_2': form.cleaned_data['answer_2'],
                'answer_3': form.cleaned_data['answer_3'],
                'correct_answer': form.cleaned_data['correct_answer'],
                'description': form.cleaned_data['description'],
                'explanation': form.cleaned_data['explanation'],
                'image': form.cleaned_data['image'],
                'learning_points': form.cleaned_data['learning_points'],
                'order': form.cleaned_data['order'],
                'question': form.cleaned_data['question'],
                'topic': form.cleaned_data['topic'],
                
            }
            db.collection("trivia").document().set(data)
            messages.success(request, 'Successfully Trivia Scenarios.') 
            return redirect('trivia_view')
        else:
            messages.error(request, 'Error creating Trivia. Please check your input.')
            return redirect('trivia_view')


from datetime import datetime

def create_users(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            data = {
                'uid': form.cleaned_data['uid'],
                'gender': form.cleaned_data['gender'],
                'email': form.cleaned_data['email'],
                'display_name': form.cleaned_data['display_name'],
                'created_time': datetime.now(),  
            }
            db.collection("users").document().set(data)
            messages.success(request, 'Successfully Users Scenarios.') 
            return redirect('users_view')
        else:
            messages.error(request, 'Error creating Users. Please check your input.')
            return redirect('users_view')


# def create_items(request):
#     if request.method == 'POST':
#         form = ItemsForm(request.POST)
#         if form.is_valid():
#             item_instance = items(
#                 data_title=form.cleaned_data['data_title'],
#                 name=form.cleaned_data['name'],
#                 data_categories=form.cleaned_data['data_categories'],
               
#             )
#             item_instance.save()
            
#             return redirect('items_view')
#     else:
#         form = ItemsForm()

#     return render(request, 'frontend/techcare_data/create_items.html', {'form': form})
def create_items(request):
    if request.method == 'POST':
        form = ItemsForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['data']
            data_title = form.cleaned_data['title']
            data_categories = form.cleaned_data['categories']

            # Create a dictionary for the data
            data = {
                'name': name,
                'data': {
                    'title': data_title,
                    'categories': data_categories,
                }
            }

            # Add the data to the Firestore collection
            db.collection("items").add(data)
            messages.success(request, 'Successfully created Items.')  
            return redirect('items_view') 
        else:
            messages.error(request, 'Error creating Items. Please check your input.')
            return redirect('items_view') 
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
 
from frontend.models import bites
import logging
from .forms import DocumentForm
from .forms import TagsForm
from django.http import JsonResponse
from .models import collection
from .models import assessmentQuestion

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

    # to restrict the user from visiting login page url if he is logged in
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

        if user is not None and not user.is_active:
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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/bites_table.html', context)

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
        form = DocumentForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'tags': form.cleaned_data['tags'],
                'difficulty': form.cleaned_data['difficulty'],
                'category': form.cleaned_data['category'],
                'content': form.cleaned_data['content'],
            }
            db.collection("bites").document().set(data)  
            return redirect('bites_view') 
    else:
        form = DocumentForm()

    return render(request, 'frontend/techcare_data/create_document.html', {'form': form})


def get_all_collections(request):
    db = firestore.client()
    all_collections = [collection.id for collection in db.collections()]

    return render(request, 'frontend/techcare_data/collections.html', {'collections': all_collections})

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

            # Check if the selected collection is in the dictionary
            if selected_collection in collection_views:
                # If yes, redirect to the corresponding view
                return redirect(collection_views[selected_collection])

    except Exception as e:
        # Handle the exception or log the error
        print(f"An error occurred: {e}")

    # Handle other cases or render the page
    return render(request, 'frontend/techcare_data/collections.html')



def activities_view(request):
    db = firestore.client()
    db = firestore.Client()
    collection = db.collection("activities")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/activities_table.html', context)


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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/badges_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/biomarkers_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/assessmentQuestion_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/categories_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/feelings_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/inAppLinks_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/inquiry_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/items_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/journal_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/journalPrompt_table.html', context)
    
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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/majorAssessment_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/psychomarkers_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/scenarios_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/shortBite_table.html', context)
    
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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/tags_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/trivia_table.html', context)

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
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/users_table.html', context)


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
        form = Tags(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['tags'],   
            }
            db.collection("tags").document().set(data)  
            return redirect('tags_view') 
    else:
        form = TagsForm()

    return render(request, 'frontend/techcare_data/create_tags.html', {'form': form})
from django.shortcuts import render
import firebase_admin
# simport pandas as pd
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from firebase import firebase
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from api.models import User
from .models import users
from django.db.models import Q
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
from django.http import HttpResponseForbidden, HttpResponse
from functools import wraps
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from import_export import resources
from django.shortcuts import render, redirect
from import_export import resources
from import_export.formats.base_formats import XLSX
from .resources import *
import openpyxl
from io import BytesIO
import pandas as pd
from django.core.files.storage import default_storage
from django.conf import settings
from pathlib import Path

db = firestore.client()
firebase_app = firebase.FirebaseApplication(
    'https://techcare-diabetes.firebaseio.com', None)


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            # Redirect to a permission denied page or login page
            return HttpResponseForbidden("Unauthorized")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


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
            form.instance.password = make_password(
                form.cleaned_data['password'])
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
            form.instance.password = make_password(
                form.cleaned_data['password'])
            form.save(commit=False)
            form.save()
            messages.success(
                request, 'Your account has been created and is pending approval.')
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
    collection = db.collection("users")
    documents = collection.stream()
    document_data = [{'id': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    query = request.GET.get('q')

    if query:
        filtered_data = []
        for entry in document_data:
            if (query.lower() in entry['data'].get('display_name', '').lower()) or \
               (query.lower() in entry['data'].get('email', '').lower()) or \
               (query.lower() in entry['data'].get('gender', '').lower()) or \
               (query.lower() in str(entry['data'].get('height', '')).lower()) or \
               (query.lower() in str(entry['data'].get('weight', '')).lower()) or \
               (query.lower() in entry['data'].get('yearOfDiagnosis', '').lower()):
                filtered_data.append(entry)
    else:
        filtered_data = document_data

    # Pagination setup
    paginator = Paginator(filtered_data, 20)  # Show 20 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/doctor/patients.html', {'page_obj': page_obj, 'query': query})


def patients_detail(request, document_name):
    db = firestore.Client()

    # Fetch user document
    user_collection = db.collection("users")
    user_document_ref = user_collection.document(document_name)
    user_document = user_document_ref.get()

    if not user_document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_data = user_document.to_dict()

    # Fetch readBites data for the user
    readbites_collection = db.collection("readBites")
    readbites_query = readbites_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    readbites_data = []
    for doc in readbites_query:
        readbites_data.append(doc.to_dict())

    readstories_collection = db.collection("readStories")
    readstories_query = readstories_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    readstories_data = []
    for doc in readstories_query:
        readstories_data.append(doc.to_dict())

    suggestedActivities_collection = db.collection("suggestedActivities")
    suggestedActivities_query = suggestedActivities_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    suggestedActivities_data = []
    for doc in suggestedActivities_query:
        suggestedActivities_data.append(doc.to_dict())

    suggestedBites_collection = db.collection("suggestedBites")
    suggestedBites_query = suggestedBites_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    suggestedBites_data = []
    for doc in suggestedBites_query:
        suggestedBites_data.append(doc.to_dict())

    suggestedInAppLinks_collection = db.collection("suggestedInAppLinks")
    suggestedInAppLinks_query = suggestedInAppLinks_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    suggestedInAppLinks_data = []
    for doc in suggestedInAppLinks_query:
        suggestedInAppLinks_data.append(doc.to_dict())

    suggestedJournals_collection = db.collection("suggestedJournals")
    suggestedJournals_query = suggestedJournals_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    suggestedJournals_data = []
    for doc in suggestedJournals_query:
        suggestedJournals_data.append(doc.to_dict())

    suggestedSelfAwarnessBites_collection = db.collection(
        "suggestedSelfAwarnessBites")
    suggestedSelfAwarnessBites_query = suggestedSelfAwarnessBites_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    suggestedSelfAwarnessBites_data = []
    for doc in suggestedSelfAwarnessBites_query:
        suggestedSelfAwarnessBites_data.append(doc.to_dict())

    suggestedWildCards_collection = db.collection("suggestedWildCards")
    suggestedWildCards_query = suggestedWildCards_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    suggestedWildCards_data = []
    for doc in suggestedWildCards_query:
        suggestedWildCards_data.append(doc.to_dict())

    selfLadder_collection = db.collection("selfLadder")
    selfLadder_query = selfLadder_collection.where(
        'userID', '==', f'/users/{document_name}').stream()
    selfLadder_data = []
    for doc in selfLadder_query:
        selfLadder_data.append(doc.to_dict())

    psychomarkers_collection = db.collection("psychomarkers")
    psychomarkers_query = psychomarkers_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    psychomarkers_data = []
    for doc in psychomarkers_query:
        psychomarkers_data.append(doc.to_dict())

    inquiry_collection = db.collection("inquiry")
    inquiry_query = inquiry_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    inquiry_data = []
    for doc in inquiry_query:
        inquiry_data.append(doc.to_dict())

    biomarkers_collection = db.collection("biomarkers")
    biomarkers_query = biomarkers_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    biomarkers_data = []
    for doc in biomarkers_query:
        biomarkers_data.append(doc.to_dict())

    dailyBloodGlucoseAverage_collection = db.collection(
        "dailyBloodGlucoseAverage")
    dailyBloodGlucoseAverage_query = dailyBloodGlucoseAverage_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    dailyBloodGlucoseAverage_data = []
    for doc in dailyBloodGlucoseAverage_query:
        dailyBloodGlucoseAverage_data.append(doc.to_dict())

    feelings_collection = db.collection("feelings")
    feelings_query = feelings_collection.where(
        'user', '==', f'/users/{document_name}').stream()
    feelings_data = []
    for doc in feelings_query:
        feelings_data.append(doc.to_dict())

        biomarkers_data = []

    # Fetch biomarkers data for the user
    biomarkers_collection = db.collection("biomarkers")
    biomarkers_query = biomarkers_collection.where(
        'user', '==', f'/users/{document_name}').stream()

    data_for_chartjs = {
        'labels': [],
        'datasets': [{
            'label': 'Blood Glucose Levels',
            'data': [],
            'borderColor': 'rgb(75, 192, 192)',
            'fill': False
        }]
    }

    for doc in biomarkers_query:
        doc_data = doc.to_dict()
        if 'time' in doc_data and 'bloodGlucose' in doc_data:
            timestamp = doc_data['time'].strftime("%Y-%m-%d %H:%M:%S")
            data_for_chartjs['labels'].append(timestamp)
            data_for_chartjs['datasets'][0]['data'].append(
                doc_data['bloodGlucose'])

        biomarkers_data.append(doc_data)  # Collect all biomarkers data

    context = {
        'document_data': document_data,
        'readbites_data': readbites_data,
        'readstories_data': readstories_data,
        'suggestedActivities_data': suggestedActivities_data,
        'suggestedBites_data': suggestedBites_data,
        'suggestedInAppLinks_data': suggestedInAppLinks_data,
        'suggestedJournals_data': suggestedJournals_data,
        'suggestedSelfAwarnessBites_data': suggestedSelfAwarnessBites_data,
        'suggestedWildCards_data': suggestedWildCards_data,
        'selfLadder_data': selfLadder_data,
        'psychomarkers_data': psychomarkers_data,
        'inquiry_data': inquiry_data,
        'biomarkers_data': biomarkers_data,
        'dailyBloodGlucoseAverage_data': dailyBloodGlucoseAverage_data,
        'data_for_chartjs': data_for_chartjs,

    }

    return render(request, 'frontend/techcare_data/patientssdocument.html', context)


@login_required(login_url='/login')
def doctor_chat_page(request):
    return render(request, 'frontend/doctor/doctor-chat.html')


@login_required(login_url='/login')
def mind_activities_view(request):
    return render(request, 'frontend/patient/activities.html')


@login_required(login_url='/login')
def quiz_question_view(request):
    return render(request, 'frontend/patient/quiz.html')


def bites_view(request):
    db = firestore.client()

    # Fetching bites data
    collection = db.collection("bites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Fetching tags data
    collection = db.collection("tags")
    documents = collection.stream()
    tags_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    form = BitesForm()

    return render(request, 'frontend/techcare_data/bites_table.html', {
        'form': form,
        'tags_data': tags_data,
        'document_data': document_data,
    })


def selfawarenessScenarios_view(request):
    db = firestore.client()
    collection = db.collection("selfawarenessScenarios")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("activities")
    documents = collection.stream()
    activity_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("selfAwarnessBites")
    documents = collection.stream()
    selfAwarnessBites_data = [
        {'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    collection = db.collection("inAppLinks")
    documents = collection.stream()
    inAppLinks_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in documents]

    collection = db.collection("journalPrompt")
    documents = collection.stream()
    journalPrompt_data = [{'name': doc.id, 'data': doc.to_dict()}
                          for doc in documents]

    collection = db.collection("bites")
    documents = collection.stream()
    bites_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    collection = db.collection("wildCard")
    documents = collection.stream()
    wildCard_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    paginator = Paginator(document_data, 20)  # Show 20 bites per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'activity_data': activity_data, 'selfAwarnessBites_data': selfAwarnessBites_data, 'inAppLinks_data': inAppLinks_data,
               'journalPrompt_data': journalPrompt_data, 'bites_data': bites_data, 'wildCard_data': wildCard_data, 'page_obj': page_obj}

    return render(request, 'frontend/techcare_data/selfawarenessScenarios_table.html', context)


def bites_view(request):
    db = firestore.client()

    # Fetching bites data
    collection = db.collection("bites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Fetching tags data
    collection = db.collection("tags")
    documents = collection.stream()
    tags_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Fetching categories data
    collection = db.collection("categories")
    documents = collection.stream()
    categories_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in documents]

    # Fetching users data
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Pagination for bites data
    paginator = Paginator(document_data, 20)  # Show 20 bites per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = BitesForm()  # Assuming BitesForm is defined in forms.py

    return render(request, 'frontend/techcare_data/bites_table.html', {
        'form': form,
        'tags_data': tags_data,
        'categories_data': categories_data,
        'users_data': users_data,
        'page_obj': page_obj,  # Pass the paginated bites data to the template
    })


def assets_view(request):
    db = firestore.client()
    collection = db.collection("assets")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    db = firestore.client()
    return render(request, 'frontend/techcare_data/assets_table.html', {'document_data': document_data})


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
            messages.error(
                request, 'Error creating Bites. Please check your input.')
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
                'selfawarenessScenarios': 'selfawarenessScenarios_view',
                'assets': 'assets_view',
                'nutrition': 'nutrition_view',
                'readBites': 'readBites_view',
                'readStories': 'readStories_view',
                'selfAwarnessBites': 'selfAwarnessBites_view',
                'selfawareness_collection': 'selfawareness_collection_view',
                'suggestedActivities': 'suggestedActivities_view',
                'suggestedBites': 'suggestedBites_view',
                'suggestedInAppLinks': 'suggestedInAppLinks_view',
                'suggestedJournals': 'suggestedJournals_view',
                'suggestedSelfAwarnessBites': 'suggestedSelfAwarnessBites_view',
                'suggestedWildCards': 'suggestedWildCards_view',
                'testTrivia': 'testTrivia_view',
                'wildCard': 'wildCard_view',
                'selfLadder': 'selfladder_view',

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

    # Fetch activities data
    activities_collection = db.collection("activities")
    activities_documents = activities_collection.stream()
    activities_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in activities_documents]

    # Paginate activities data
    activities_paginator = Paginator(
        activities_data, 20)  # Show 10 activities per page
    activities_page_number = request.GET.get('activities_page')
    activities_page_obj = activities_paginator.get_page(activities_page_number)

    form = ActivitiesForm()

    # Fetch tags data
    tags_collection = db.collection("tags")
    tags_documents = tags_collection.stream()
    tags_data = [{'name': doc.id, 'data': doc.to_dict()}
                 for doc in tags_documents]

    # Paginate tags data
    tags_paginator = Paginator(tags_data, 20)  # Show 10 tags per page
    tags_page_number = request.GET.get('tags_page')
    tags_page_obj = tags_paginator.get_page(tags_page_number)

    return render(request, 'frontend/techcare_data/activities_table.html', {
        'form': form,
        'tags_data': tags_page_obj,
        'activities_page_obj': activities_page_obj
    })


def assets_view(request):
    db = firestore.Client()
    collection = db.collection("assets")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    paginator = Paginator(document_data, 20)  # 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/assets_table.html', {'page_obj': page_obj})


def nutrition_view(request):
    db = firestore.client()
    db = firestore.Client()

    # Fetching nutrition data
    collection = db.collection("nutrition")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Implementing pagination for nutrition data
    # Show 20 nutrition entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = NutritionForm()
    return render(request, 'frontend/techcare_data/nutrition_table.html', {
        'form': form,
        'page_obj': page_obj
    })


def readBites_view(request):
    db = firestore.Client()

    # Fetching readBites data
    collection = db.collection("readBites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Fetching users data
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Fetching bites data
    collection = db.collection("bites")
    documents = collection.stream()
    bites_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Implementing pagination for readBites data
    # Show 20 readBites entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/readBites_table.html', {
        'document_data': document_data,
        'users_data': users_data,
        'bites_data': bites_data,
        'page_obj': page_obj,  # Pass page_obj to template for pagination
    })


def readStories_view(request):
    db = firestore.Client()

    # Fetching readStories data
    collection = db.collection("readStories")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Fetching users data
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Fetching selfawarenessScenarios data
    collection = db.collection("selfawarenessScenarios")
    documents = collection.stream()
    selfawarenessScenarios_data = [
        {'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Implementing pagination for readStories data
    # Show 20 readStories entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/readStories_table.html', {
        'document_data': document_data,
        'users_data': users_data,
        'selfawarenessScenarios_data': selfawarenessScenarios_data,
        'page_obj': page_obj,  # Pass page_obj to template for pagination
    })


def selfAwarnessBites_view(request):
    db = firestore.client()
    collection = db.collection("selfAwarnessBites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/selfAwarnessBites_table.html', {'page_obj': page_obj})


def selfawareness_collection_view(request):
    db = firestore.client()
    collection = db.collection("selfawareness_collection")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/selfawareness_collection_table.html', {'page_obj': page_obj})


def suggestedActivities_view(request):
    db = firestore.client()
    collection = db.collection("suggestedActivities")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    collection = db.collection("activities")
    documents = collection.stream()
    activities_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in documents]

    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/suggestedActivities_table.html', {'page_obj': page_obj, 'users_data': users_data, 'activities_data': activities_data})


def suggestedBites_view(request):
    db = firestore.client()
    collection = db.collection("suggestedBites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    collection = db.collection("bites")
    documents = collection.stream()
    bites_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    collection = db.collection("selfAwarnessBites")
    documents = collection.stream()
    selfAwarnessBites_data = [
        {'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    return render(request, 'frontend/techcare_data/suggestedBites_table.html', {'document_data': document_data, 'users_data': users_data, 'bites_data': bites_data, 'selfAwarnessBites_data': selfAwarnessBites_data})


def suggestedInAppLinks_view(request):
    db = firestore.client()
    collection = db.collection("suggestedInAppLinks")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    collection = db.collection("inAppLinks")
    documents = collection.stream()
    inAppLinks_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in documents]

    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/suggestedInAppLinks_table.html', {'page_obj': page_obj, 'users_data': users_data, 'inAppLinks_data': inAppLinks_data})


def suggestedJournals_view(request):
    db = firestore.client()
    collection = db.collection("suggestedJournals")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    collection = db.collection("journalPrompt")
    documents = collection.stream()
    journalPrompt_data = [{'name': doc.id, 'data': doc.to_dict()}
                          for doc in documents]
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/suggestedJournals_table.html', {'page_obj': page_obj, 'users_data': users_data, 'journalPrompt_data': journalPrompt_data})


def suggestedSelfAwarnessBites_view(request):
    db = firestore.client()
    collection = db.collection("suggestedSelfAwarnessBites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    collection = db.collection("selfAwarnessBites")
    documents = collection.stream()
    selfAwarnessBites_data = [
        {'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/suggestedSelfAwarnessBites_table.html', {'page_obj': page_obj, 'users_data': users_data, 'selfAwarnessBites_data': selfAwarnessBites_data})


def suggestedWildCards_view(request):
    db = firestore.client()
    collection = db.collection("suggestedWildCards")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    collection = db.collection("wildCard")
    documents = collection.stream()
    wildCard_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/suggestedWildCards_table.html', {'page_obj': page_obj, 'users_data': users_data, 'wildCard_data': wildCard_data})


def selfladder_view(request):
    db = firestore.client()
    collection = db.collection("selfLadder")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Show 20 readStories entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/selfladder_table.html', {'page_obj': page_obj, 'users_data': users_data})


def testTrivia_view(request):
    db = firestore.client()
    collection = db.collection("testTrivia")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    # Show 20 readStories entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/testTrivia_table.html', {'page_obj': page_obj})


def wildCard_view(request):
    db = firestore.client()
    collection = db.collection("wildCard")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Show 20 readStories entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'frontend/techcare_data/wildCard_table.html', {'page_obj': page_obj})


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
    collection = db.collection("badges")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    paginator = Paginator(document_data, 20)  # Show 20 badges per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = BadgesForm()  # Assuming BadgesForm is defined in forms.py

    return render(request, 'frontend/techcare_data/badges_table.html', {'form': form, 'page_obj': page_obj})


def badgesdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("badges")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/badgesdocument.html', {'document_data': document_data})


def biomarkers_view(request):

    # Fetch biomarkers data
    biomarkers_collection = db.collection("biomarkers")
    biomarkers_documents = biomarkers_collection.stream()
    biomarkers_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in biomarkers_documents]

    # Paginate biomarkers data
    biomarkers_paginator = Paginator(
        biomarkers_data, 20)  # Show 10 biomarkers per page
    biomarkers_page_number = request.GET.get('biomarkers_page')
    biomarkers_page_obj = biomarkers_paginator.get_page(biomarkers_page_number)

    form = BiomarkersForm()

    # Fetch users data
    users_collection = db.collection("users")
    users_documents = users_collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()}
                  for doc in users_documents]

    # Paginate users data
    users_paginator = Paginator(users_data, 20)  # Show 10 users per page
    users_page_number = request.GET.get('users_page')
    users_page_obj = users_paginator.get_page(users_page_number)

    return render(request, 'frontend/techcare_data/biomarkers_table.html', {
        'form': form,
        'biomarkers_page_obj': biomarkers_page_obj,
        'users_data': users_page_obj
    })


def biomarkersdocument_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("biomarkers")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:

        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/biomarkersdocument.html', {'document_data': document_data})


def assessmentQuestion_view(request):
    db = firestore.Client()

    # Fetch assessmentQuestion data
    assessment_collection = db.collection("assessmentQuestion")
    assessment_documents = assessment_collection.stream()
    assessment_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in assessment_documents]

    # Paginate assessmentQuestion data
    # Show 10 assessment questions per page
    assessment_paginator = Paginator(assessment_data, 20)
    assessment_page_number = request.GET.get('assessment_page')
    assessment_page_obj = assessment_paginator.get_page(assessment_page_number)

    form = AssessmentQuestionForm()

    # Fetch majorAssessment data
    major_collection = db.collection("majorAssessment")
    major_documents = major_collection.stream()
    major_data = [{'name': doc.id, 'data': doc.to_dict()}
                  for doc in major_documents]

    # Paginate majorAssessment data
    # Show 10 major assessments per page
    major_paginator = Paginator(major_data, 20)
    major_page_number = request.GET.get('major_page')
    major_page_obj = major_paginator.get_page(major_page_number)

    return render(request, 'frontend/techcare_data/assessmentQuestion_table.html', {
        'form': form,
        'majorAssessment': major_page_obj,
        'assessment_page_obj': assessment_page_obj
    })


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Pagination
    paginator = Paginator(document_data, 20)  # Show 20 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = CategoriesForm()
    return render(request, 'frontend/techcare_data/categories_table.html', {
        'page_obj': page_obj,
        'form': form
    })


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    collection2 = db.collection("user")
    documents2 = collection2.stream()
    feelings = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents2]

    # Pagination for feelings
    paginator = Paginator(document_data, 20)  # Show 20 feelings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = FeelingsForm()
    return render(request, 'frontend/techcare_data/feelings_table.html', {
        'form': form,
        'feelings': feelings,
        'page_obj': page_obj
    })


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Pagination for inAppLinks
    paginator = Paginator(document_data, 20)  # Show 20 inAppLinks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = InAppLinksForm()
    return render(request, 'frontend/techcare_data/inAppLinks_table.html', {
        'form': form,
        'page_obj': page_obj
    })


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

    # Fetching inquiry data
    collection = db.collection("inquiry")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Fetching users data
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Implementing pagination for inquiry data
    paginator = Paginator(document_data, 20)  # Show 20 inquiries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = InquiryForm()
    return render(request, 'frontend/techcare_data/inquiry_table.html', {
        'form': form,
        'page_obj': page_obj,
        'users_data': users_data
    })


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

    # Fetching items data
    collection = db.collection("items")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Implementing pagination for items data
    paginator = Paginator(document_data, 20)  # Show 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = ItemsForm()
    return render(request, 'frontend/techcare_data/items_table.html', {
        'form': form,
        'page_obj': page_obj
    })


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

    # Fetching journal data
    collection = db.collection("journal")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Implementing pagination for journal data
    # Show 20 journal entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = JournalForm()
    return render(request, 'frontend/techcare_data/journal_table.html', {
        'form': form,
        'page_obj': page_obj
    })


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

    # Fetching journalPrompt data
    collection = db.collection("journalPrompt")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Implementing pagination for journalPrompt data
    # Show 20 journalPrompt entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = JournalForm()
    return render(request, 'frontend/techcare_data/journalPrompt_table.html', {
        'form': form,
        'page_obj': page_obj
    })


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

    # Fetching majorAssessment data
    collection = db.collection("majorAssessment")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Implementing pagination for majorAssessment data
    # Show 20 majorAssessment entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = MajorAssessmentForm()
    return render(request, 'frontend/techcare_data/majorAssessment_table.html', {
        'form': form,
        'page_obj': page_obj
    })


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

    # Fetching psychomarkers data
    collection = db.collection("psychomarkers")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]

    # Implementing pagination for psychomarkers data
    # Show 20 psychomarkers entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetching users data
    collection = db.collection("users")
    documents = collection.stream()
    users_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    form = PsychomarkersForm()
    return render(request, 'frontend/techcare_data/psychomarkers_table.html', {
        'form': form,
        'page_obj': page_obj,
        'users_data': users_data
    })


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    form = ScenariosForm()

    collection = db.collection("majorAssessment")
    documents = collection.stream()
    majorAssessment_data = [
        {'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    collection = db.collection("activities")
    documents = collection.stream()
    activities_data = [{'name': doc.id, 'data': doc.to_dict()}
                       for doc in documents]

    collection = db.collection("suggestedBites")
    documents = collection.stream()
    suggestedBites_data = [{'name': doc.id, 'data': doc.to_dict()}
                           for doc in documents]

    collection = db.collection("suggestedJournals")
    documents = collection.stream()
    suggestedJournals_data = [
        {'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    # Show 20 scenarios entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    collection = db.collection("bites")
    documents = collection.stream()
    bites_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]

    return render(request, 'frontend/techcare_data/scenarios_table.html', {'page_obj': page_obj, 'form': form, 'majorAssessment_data': majorAssessment_data, 'activities_data': activities_data, 'suggestedBites_data': suggestedBites_data, 'suggestedJournals_data': suggestedJournals_data, 'bites_data': bites_data})


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    form = ShortBiteForm()

    # Show 20 scenarios entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/techcare_data/shortBite_table.html', {'page_obj': page_obj, 'form': form})


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    form = TagsForm()

    # Show 20 scenarios entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'frontend/techcare_data/tags_table.html', {'page_obj': page_obj, 'form': form})


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    form = TriviaForm()
    # Show 20 scenarios entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'frontend/techcare_data/trivia_table.html', {'page_obj': page_obj, 'form': form})


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
    document_data = [{'name': doc.id, 'data': doc.to_dict()}
                     for doc in documents]
    form = UsersForm()
    # Show 20 scenarios entries per page
    paginator = Paginator(document_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'frontend/techcare_data/users_table.html', {'page_obj': page_obj, 'form': form})


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
            messages.error(
                request, 'Error creating Tags. Please check your input.')
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
            messages.error(
                request, 'Error creating activity. Please check your input.')
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
            messages.success(
                request, 'Successfully created Assessment Question.')
            return redirect('assessmentQuestion_view')
        else:
            messages.error(
                request, 'Error creating Assessment Question. Please check your input.')
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
            messages.error(
                request, 'Error creating Badges View. Please check your input.')
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
            messages.error(
                request, 'Error creating Biomarkers View. Please check your input.')
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
            messages.error(
                request, 'Error creating Categories. Please check your input.')
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
            messages.error(
                request, 'Error creating Feelings. Please check your input.')
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
            messages.error(
                request, 'Error creating inAppLinks. Please check your input.')
            return redirect('inAppLinks_view')

    return render(request, 'frontend/techcare_data/create_inAppLinks.html', {'form': form})


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
            messages.error(
                request, 'Error creating Inquiry. Please check your input.')
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
            messages.error(
                request, 'Error creating Journal. Please check your input.')
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
            messages.error(
                request, 'Error creating JournalPrompt. Please check your input.')
            return redirect('journalPrompt_view')


def create_majorAssessment(request):
    if request.method == 'POST':
        form = MajorAssessmentForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'numberOfQuestions': form.cleaned_data['numberOfQuestions'],
                'description': form.cleaned_data['description'],
                # Removed the space before 'order'
                'order': form.cleaned_data['order'],
            }
            db.collection("majorAssessment").document().set(data)
            messages.success(request, 'Successfully created MajorAssessment.')
            return redirect('majorAssessment_view')
        else:
            messages.error(
                request, 'Error creating MajorAssessment. Please check your input.')
            return redirect('majorAssessment_view')


def create_psychomarkers(request):
    if request.method == 'POST':
        form = PsychomarkersForm(request.POST)
        if form.is_valid():
            # user_id = form.cleaned_data['user'].id
            data = {
                'time': datetime.now(),
                # Assuming 'user' is a ForeignKey in your model, use the user_id
                'user': request.POST.get('user_id'),
                'depression': form.cleaned_data['depression'],
            }
            db.collection("psychomarkers").document().set(data)
            messages.success(request, 'Successfully created Psychomarkers.')
            return redirect('psychomarkers_view')
        else:
            messages.error(
                request, 'Error creating Psychomarkers. Please check your input.')
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
            messages.error(
                request, 'Error creating Scenarios. Please check your input.')
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
            messages.error(
                request, 'Error creating ShortBite. Please check your input.')
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
            messages.error(
                request, 'Error creating Trivia. Please check your input.')
            return redirect('trivia_view')


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
            messages.success(request, 'Successfully Create Nutrition.')
            return redirect('users_view')
        else:
            messages.error(
                request, 'Error creating Nutrition. Please check your input.')
            return redirect('users_view')


def create_nutrition(request):
    if request.method == 'POST':
        form = NutritionForm(request.POST)
        if form.is_valid():
            data = {
                'carbContent': request.POST.get('carbContent'),
                'name_ar': request.POST.get('name_ar'),
                'name_en': request.POST.get('name_en'),
                'portion': request.POST.get('portion'),
                'proteinContent': request.POST.get('proteinContent'),
                'totalCalories': request.POST.get('totalCalories'),
                'weight': request.POST.get('weight'),
            }
            db.collection("nutrition").document().set(data)
            messages.success(request, 'Successfully Users Scenarios.')
            return redirect('nutrition_view')
        else:
            messages.error(
                request, 'Error creating Nutrition. Please check your input.')
            return redirect('nutrition_view')


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
            messages.error(
                request, 'Error creating Items. Please check your input.')
            return redirect('items_view')
    return render(request, 'frontend/techcare_data/activitiesdocument.html', {'document_data': document_data})


def activities_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("activities")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Activity deleted successfully!')
    return redirect('activities_view')


def assessmentQuestion_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("assessmentQuestion")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'AssessmentQuestion deleted successfully!')
    return redirect('assessmentQuestion_view')


def badges_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("badges")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Badges deleted successfully!')
    return redirect('badges_view')


def biomarkers_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("biomarkers_delete")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Biomarkers deleted successfully!')
    return redirect('biomarkers_view')


def bites_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("bites")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Bites deleted successfully!')
    return redirect('bites_view')


def categories_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("categories")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Categories deleted successfully!')
    return redirect('categories_view')


def feelings_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("feelings")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Feelings deleted successfully!')
    return redirect('feelings_view')


def inAppLinks_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("inAppLinks")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'InAppLinks deleted successfully!')
    return redirect('inAppLinks_view')


def inquiry_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("inquiry")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Inquiry deleted successfully!')
    return redirect('inquiry_view')


def items_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("items")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Items deleted successfully!')
    return redirect('items_view')


def journal_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("journal")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Journal deleted successfully!')
    return redirect('journal_view')


def journalPrompt_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("journalPrompt")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'JournalPrompt deleted successfully!')
    return redirect('journalPrompt_view')


def majorAssessment_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("majorAssessment")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'MajorAssessment deleted successfully!')
    return redirect('majorAssessment_view')


def psychomarkers_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("psychomarkers")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Psychomarkers deleted successfully!')
    return redirect('psychomarkers_view')


def scenarios_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("scenarios")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Scenarios deleted successfully!')
    return redirect('scenarios_view')


def shortBite_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("shortBite")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'ShortBite deleted successfully!')
    return redirect('shortBite_view')


def tags_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("tags")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Tags deleted successfully!')
    return redirect('tags_view')


def trivia_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("trivia")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'Trivia deleted successfully!')
    return redirect('trivia_view')


def users_delete(request, document_name):
    db = firestore.Client()
    collection = db.collection("users")
    document_ref = collection.document(document_name)
    document = document_ref.get()

    if not document.exists:
        return render(request, 'frontend/techcare_data/document_not_found.html')

    document_ref.delete()

    messages.success(request, 'User deleted successfully!')
    return redirect('users_view')

# def _delete(request, document_name):
#     db = firestore.Client()
#     collection = db.collection("")
#     document_ref = collection.document(document_name)
#     document = document_ref.get()

#     if not document.exists:
#         return render(request, 'frontend/techcare_data/document_not_found.html')

#     document_ref.delete()

#     messages.success(request, ' deleted successfully!')
#     return redirect('_view')


def update_activities(request, document_name):
    if request.method == 'POST':
        form = ActivitiesForm(request.POST)
        entry_id = document_name
        data = {
            'tags': request.POST.get('tags'),
            'description': request.POST.get('description'),
            'title': request.POST.get('title'),
            'duration': request.POST.get('duration'),
            'type': request.POST.get('type'),
            'track': request.POST.get('track'),
            'audiotrackId': request.POST.get('audiotrackId'),
            'audiotrackTitle': request.POST.get('audiotrackTitle'),
            'label': request.POST.get('label'),

        }
        db = firestore.client()
        db.collection("activities").document(entry_id).update(data)
        messages.success(request, 'Activity updated successfully.')
        return redirect('activities_view')
    else:
        messages.error(
            request, 'Error updating activity. Please check your input.')
        return redirect('activities_view')


def update_assessmentQuestion(request, document_name):
    if request.method == 'POST':
        form = AssessmentQuestionForm(request.POST)
        entry_id = document_name
        data = {
            'majorAssessment': request.POST.get('majorAssessment'),
            'max': request.POST.get('max'),
            'order': request.POST.get('order'),
            'points': request.POST.get('points'),
            'question': request.POST.get('question'),
        }
        db = firestore.client()
        db.collection("assessmentQuestion").document(entry_id).update(data)
        messages.success(request, 'assessmentQuestion updated successfully.')
        return redirect('assessmentQuestion_view')
    else:
        messages.error(
            request, 'Error updating assessmentQuestion. Please check your input.')
        return redirect('assessmentQuestion_view')


def update_badges(request, document_name):
    if request.method == 'POST':
        form = BadgesForm(request.POST)
        entry_id = document_name
        data = {
            'title': request.POST.get('title'),
        }
        db = firestore.client()
        db.collection("badges").document(entry_id).update(data)
        messages.success(request, 'badges updated successfully.')
        return redirect('badges_view')
    else:
        messages.error(
            request, 'Error updating badges. Please check your input.')
        return redirect('badges_view')


def update_biomarkers(request, document_name):
    if request.method == 'POST':
        form = BiomarkersForm(request.POST)
        entry_id = document_name
        data = {
            'bloodGlucose': request.POST.get('bloodGlucose'),
            'bloodGlucoseType': request.POST.get('bloodGlucoseType'),
            'dailyActivity': request.POST.get('dailyActivity'),
            'dailyCarbs': request.POST.get('dailyCarbs'),
            'weeklyActivity': request.POST.get('weeklyActivity'),
            'sleepQuality': request.POST.get('sleepQuality'),
            'time': request.POST.get('time'),
            'user': request.POST.get('user'),
            'weight': request.POST.get('weight'),
            'FBS': request.POST.get('FBS'),
            'HBA1c': request.POST.get('HBA1c'),
        }
        db = firestore.client()
        db.collection("biomarkers").document(entry_id).update(data)
        messages.success(request, ' biomarkers updated successfully.')
        return redirect('biomarkers_view')
    else:
        messages.error(
            request, 'Error updating  biomarkers . Please check your input.')
        return redirect('biomarkers_view')


def update_bites(request, document_name):
    if request.method == 'POST':
        form = BitesForm(request.POST)
        entry_id = document_name
        data = {
            'image': request.POST.get('image'),
            'order': request.POST.get('order'),
            'Learning_ponits': request.POST.get('Learning_ponits'),
            'CBT_points': request.POST.get('CBT_points'),
            'next': request.POST.get('next'),
            'scenarioID': request.POST.get('scenarioID'),
            'thumbs_up_users': request.POST.get('thumbs_up_users'),
            'thumbs_down_users': request.POST.get('thumbs_down_users'),
            'categories': request.POST.get('categories'),
            'content': request.POST.get('content'),
            'difficulty': request.POST.get('difficulty'),
            'tags': request.POST.get('tags'),
            'title': request.POST.get('title'),
        }
        db = firestore.client()
        db.collection("bites").document(entry_id).update(data)
        messages.success(request, 'bites updated successfully.')
        return redirect('bites_view')
    else:
        messages.error(
            request, 'Error updating bites  . Please check your input.')
        return redirect('bites_view')


def update_categories(request, document_name):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        entry_id = document_name
        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
        }
        db = firestore.client()
        db.collection("categories").document(entry_id).update(data)
        messages.success(request, ' categories updated successfully.')
        return redirect('categories_view')
    else:
        messages.error(
            request, 'Error updating  categories . Please check your input.')
        return redirect('categories_view')


def update_feelings(request, document_name):
    if request.method == 'POST':
        form = FeelingsForm(request.POST)
        entry_id = document_name
        data = {
            'anger': request.POST.get('anger'),
            'fear': request.POST.get('fear'),
            'happiness': request.POST.get('happiness'),
            'joy': request.POST.get('joy'),
            'love': request.POST.get('love'),
            'sadness': request.POST.get('sadness'),
            'shame': request.POST.get('shame'),
            'strength': request.POST.get('strength'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),
        }
        db = firestore.client()
        db.collection("feelings").document(entry_id).update(data)
        messages.success(request, 'feelings updated successfully.')
        return redirect('feelings_view')
    else:
        messages.error(
            request, 'Error updating feelings . Please check your input.')
        return redirect('feelings_view')


def update_inAppLinks(request, document_name):
    if request.method == 'POST':
        form = InAppLinksForm(request.POST)
        entry_id = document_name
        data = {
            'description': request.POST.get('description'),
            'title': request.POST.get('title'),
            'order': request.POST.get('order'),
            'type': request.POST.get('type'),
            'image': request.POST.get('image'),
            'link': request.POST.get('link'),
        }
        db = firestore.client()
        db.collection("inAppLinks").document(entry_id).update(data)
        messages.success(request, 'inAppLinks updated successfully.')
        return redirect('inAppLinks_view')
    else:
        messages.error(
            request, 'Error updating inAppLinks . Please check your input.')
        return redirect('inAppLinks_view')


def update_inquiry(request, document_name):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        entry_id = document_name
        data = {
            'answer': request.POST.get('answer'),
            'question': request.POST.get('question'),
            'time': request.POST.get('time'),
            'topic': request.POST.get('topic'),
            'user': request.POST.get('user'),
        }
        db = firestore.client()
        db.collection("inquiry").document(entry_id).update(data)
        messages.success(request, 'inquiry updated successfully.')
        return redirect('inquiry_view')
    else:
        messages.error(
            request, 'Error updating inquiry . Please check your input.')
        return redirect('inquiry_view')


def update_items(request, document_name):
    if request.method == 'POST':
        form = ItemsForm(request.POST)
        entry_id = document_name
        data = {
            'title': request.POST.get('title'),
            'data': request.POST.get('data'),
            'categories': request.POST.get('categories'),
        }
        db = firestore.client()
        db.collection("items").document(entry_id).update(data)
        messages.success(request, 'items updated successfully.')
        return redirect('items_view')
    else:
        messages.error(
            request, 'Error updating items . Please check your input.')
        return redirect('items_view')


def update_journal(request, document_name):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        entry_id = document_name
        data = {
            'description': request.POST.get('description'),
            'title': request.POST.get('title'),
        }
        db = firestore.client()
        db.collection("journal").document(entry_id).update(data)
        messages.success(request, 'journal updated successfully.')
        return redirect('journal_view')
    else:
        messages.error(
            request, 'Error updating journal . Please check your input.')
        return redirect('journal_view')


def update_journalPrompt(request, document_name):
    if request.method == 'POST':
        form = JournalPromptForm(request.POST)
        entry_id = document_name
        data = {
            'title': request.POST.get('title'),
        }
        db = firestore.client()
        db.collection("journalPrompt").document(entry_id).update(data)
        messages.success(request, 'journalPrompt updated successfully.')
        return redirect('journalPrompt_view')
    else:
        messages.error(
            request, 'Error updating journalPrompt . Please check your input.')
        return redirect('journalPrompt_view')


def update_majorAssessment(request, document_name):
    if request.method == 'POST':
        form = MajorAssessmentForm(request.POST)
        entry_id = document_name
        data = {
            'description': request.POST.get('description'),
            'numberOfQuestions': request.POST.get('numberOfQuestions'),
            'order': request.POST.get('order'),
            'title': request.POST.get('title'),
        }
        db = firestore.client()
        db.collection("majorAssessment").document(entry_id).update(data)
        messages.success(request, 'majorAssessment updated successfully.')
        return redirect('majorAssessment_view')
    else:
        messages.error(
            request, 'Error updating majorAssessment . Please check your input.')
        return redirect('majorAssessment_view')


def update_psychomarkers(request, document_name):
    if request.method == 'POST':
        form = PsychomarkersForm(request.POST)
        entry_id = document_name
        data = {
            'time': request.POST.get('time'),
            'user': request.POST.get('user'),
            'depression': request.POST.get('depression'),
        }
        db = firestore.client()
        db.collection("psychomarkers").document(entry_id).update(data)
        messages.success(request, 'psychomarkers updated successfully.')
        return redirect('psychomarkers_view')
    else:
        messages.error(
            request, 'Error updating psychomarkers . Please check your input.')
        return redirect('psychomarkers_view')


def update_scenarios(request, document_name):
    if request.method == 'POST':
        form = ScenariosForm(request.POST)
        entry_id = document_name
        data = {
            'PositiveCorrectionAlternative': request.POST.get('PositiveCorrectionAlternative'),
            'actionreply': request.POST.get('actionreply'),
            'correction': request.POST.get('correction'),
            'positiveActionReply': request.POST.get('positiveActionReply'),
            'title': request.POST.get('title'),
            'majorAssessment': request.POST.get('majorAssessment'),
            'suggestedActivity': request.POST.get('suggestedActivity'),
            'type': request.POST.get('type'),

            'suggestedBite': request.POST.get('suggestedBite'),
            'suggestedJournal': request.POST.get('suggestedJournal'),
            'max': request.POST.get('max'),
            'feeling': request.POST.get('feeling'),
            'status': request.POST.get('status'),
            'order': request.POST.get('order'),
            'story': request.POST.get('story'),
            'InteractiveStatement': request.POST.get('InteractiveStatement'),
            'Recommendation': request.POST.get('Recommendation'),
            'SuggestBitesFromBank': request.POST.get('SuggestBitesFromBank'),

        }
        db = firestore.client()
        db.collection("scenarios").document(entry_id).update(data)
        messages.success(request, 'scenarios updated successfully.')
        return redirect('scenarios_view')
    else:
        messages.error(
            request, 'Error updating scenarios . Please check your input.')
        return redirect('scenarios_view')


def update_shortBite(request, document_name):
    if request.method == 'POST':
        form = ShortBiteForm(request.POST)
        entry_id = document_name
        data = {
            'order': request.POST.get('order'),
            'title': request.POST.get('title'),
        }
        db = firestore.client()
        db.collection("shortBite").document(entry_id).update(data)
        messages.success(request, 'shortBite updated successfully.')
        return redirect('shortBite_view')
    else:
        messages.error(
            request, 'Error updating shortBite . Please check your input.')
        return redirect('shortBite_view')


def update_tags(request, document_name):
    if request.method == 'POST':
        form = TagsForm(request.POST)
        entry_id = document_name
        data = {
            'description': request.POST.get('description'),
            'image': request.POST.get('image'),
            'title': request.POST.get('title'),
        }
        db = firestore.client()
        db.collection("tags").document(entry_id).update(data)
        messages.success(request, 'tags updated successfully.')
        return redirect('tags_view')
    else:
        messages.error(
            request, 'Error updating tags  . Please check your input.')
        return redirect('tags_view')


def update_trivia(request, document_name):
    if request.method == 'POST':
        form = TriviaForm(request.POST)
        entry_id = document_name
        data = {
            'CBT_points': request.POST.get('CBT_points'),
            'answer_1': request.POST.get('answer_1'),
            'answer_2': request.POST.get('answer_2'),
            'answer_3': request.POST.get('answer_3'),
            'correct_answer': request.POST.get('correct_answer'),
            'description': request.POST.get('description'),
            'explanation': request.POST.get('explanation'),
            'image': request.POST.get('image'),
            'question': request.POST.get('question'),
            'learning_points': request.POST.get('learning_points'),
            'order': request.POST.get('order'),
            'topic': request.POST.get('topic'),
        }
        db = firestore.client()
        db.collection("trivia").document(entry_id).update(data)
        messages.success(request, 'trivia updated successfully.')
        return redirect('trivia_view')
    else:
        messages.error(
            request, 'Error updating trivia  . Please check your input.')
        return redirect('trivia_view')


def update_users(request, document_name):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        entry_id = document_name
        data = {
            'email': request.POST.get('email'),
            'created_time': request.POST.get('created_time'),
            'gender': request.POST.get('gender'),
            'uid': request.POST.get('uid'),
            'display_name': request.POST.get('display_name'),
        }
        db = firestore.client()
        db.collection("users").document(entry_id).update(data)
        messages.success(request, 'users updated successfully.')
        return redirect('users_view')
    else:
        messages.error(
            request, 'Error updating users  . Please check your input.')
        return redirect('users_view')


def update_selfawarenessScenarios(request, document_name):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        entry_id = document_name
        data = {
            'activity': request.POST.get('activity'),
            'biteID': request.POST.get('biteID'),
            'correction1from0to2': request.POST.get('correction1from0to2'),
            'correction2from3to5': request.POST.get('correction2from3to5'),
            'inAppLink': request.POST.get('inAppLink'),
            'interactiveStatement': request.POST.get('interactiveStatement'),
            'journal': request.POST.get('journal'),
            'normalBite': request.POST.get('normalBite'),
            'recommendation1': request.POST.get('recommendation1'),
            'recommendation2': request.POST.get('recommendation2'),
            'scenarioID': request.POST.get('scenarioID'),
            'story': request.POST.get('story'),
            'storyTitle': request.POST.get('storyTitle'),
            'wildcard': request.POST.get('wildcard'),
        }
        db = firestore.client()
        db.collection("selfawarenessScenarios").document(entry_id).update(data)
        messages.success(
            request, 'selfawarenessScenarios updated successfully.')
        return redirect('selfawarenessScenarios_view')
    else:
        messages.error(
            request, 'Error updating selfawarenessScenarios  . Please check your input.')
        return redirect('selfawarenessScenarios_view')


def update_assets(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'assetsType': request.POST.get('assetsType'),
            'label': request.POST.get('label'),
            'name': request.POST.get('name'),
            'path': request.POST.get('path'),
        }
        db = firestore.client()
        db.collection("assets").document(entry_id).update(data)
        messages.success(request, 'assets updated successfully.')
        return redirect('assets_view')
    else:
        messages.error(
            request, 'Error updating assets  . Please check your input.')
        return redirect('assets_view')


def update_nutrition(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'carbContent': request.POST.get('carbContent'),
            'name_ar': request.POST.get('name_ar'),
            'name_en': request.POST.get('name_en'),
            'portion': request.POST.get('portion'),
            'proteinContent': request.POST.get('proteinContent'),
            'totalCalories': request.POST.get('totalCalories'),
            'weight': request.POST.get('weight'),
        }
        db = firestore.client()
        db.collection("nutrition").document(entry_id).update(data)
        messages.success(request, 'nutrition updated successfully.')
        return redirect('nutrition_view')
    else:
        messages.error(
            request, 'Error updating nutrition . Please check your input.')
        return redirect('nutrition_view')


def update_readBites(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'bite': request.POST.get('bite'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),
        }
        db = firestore.client()
        db.collection("readBites").document(entry_id).update(data)
        messages.success(request, 'readBites updated successfully.')
        return redirect('readBites_view')
    else:
        messages.error(
            request, 'Error updating readBites  . Please check your input.')
        return redirect('readBites_view')


def update_readStories(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'senario': request.POST.get('senario'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),
        }
        db = firestore.client()
        db.collection("readStories").document(entry_id).update(data)
        messages.success(request, 'readStories updated successfully.')
        return redirect('readStories_view')
    else:
        messages.error(
            request, 'Error updating readStories  . Please check your input.')
        return redirect('readStories_view')


def update_selfAwarnessBites(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'scenarioID': request.POST.get('scenarioID'),
            'selfawarenessBiteText': request.POST.get('selfawarenessBiteText'),
            'selfawarenessBiteTitle': request.POST.get('selfawarenessBiteTitle'),
            'tags': request.POST.get('tags'),
        }
        db = firestore.client()
        db.collection("selfAwarnessBites").document(entry_id).update(data)
        messages.success(request, 'selfAwarnessBites updated successfully.')
        return redirect('selfAwarnessBites_view')
    else:
        messages.error(
            request, 'Error updating selfAwarnessBites  . Please check your input.')
        return redirect('selfAwarnessBites_view')


def update_selfawareness_collection(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'selfawareness_bite_text': request.POST.get('selfawareness_bite_text'),
            'tags': request.POST.get('tags'),
        }
        db = firestore.client()
        db.collection("selfawareness_collection").document(
            entry_id).update(data)
        messages.success(
            request, 'selfawareness_collection updated successfully.')
        return redirect('selfawareness_collection_view')
    else:
        messages.error(
            request, 'Error updating selfawareness_collection   . Please check your input.')
        return redirect('selfawareness_collection_view')


def update_suggestedActivities(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'activity': request.POST.get('activity'),
            'state': request.POST.get('state'),
            'type': request.POST.get('type'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),

        }
        db = firestore.client()
        db.collection("suggestedActivities").document(entry_id).update(data)
        messages.success(request, 'suggestedActivities updated successfully.')
        return redirect('suggestedActivities_view')
    else:
        messages.error(
            request, 'Error updating suggestedActivities   . Please check your input.')
        return redirect('suggestedActivities_view')


def update_suggestedBites(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'bite': request.POST.get('bite'),
            'state': request.POST.get('state'),
            'user': request.POST.get('user'),
            'selfAwarnessBite': request.POST.get('selfAwarnessBite'),
            'time': request.POST.get('time'),

        }
        db = firestore.client()
        db.collection("suggestedBites").document(entry_id).update(data)
        messages.success(request, 'suggestedBites updated successfully.')
        return redirect('suggestedBites_view')
    else:
        messages.error(
            request, 'Error updating  suggestedBites . Please check your input.')
        return redirect('suggestedBites_view')


def update_suggestedInAppLinks(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'inAppLink': request.POST.get('inAppLink'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),

        }
        db = firestore.client()
        db.collection("suggestedInAppLinks").document(entry_id).update(data)
        messages.success(request, 'suggestedInAppLinks updated successfully.')
        return redirect('suggestedInAppLinks_view')
    else:
        messages.error(
            request, 'Error updating suggestedInAppLinks  . Please check your input.')
        return redirect('suggestedInAppLinks_view')


def update_suggestedJournals(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'journal': request.POST.get('journal'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),

        }
        db = firestore.client()
        db.collection("suggestedJournals").document(entry_id).update(data)
        messages.success(request, 'suggestedJournals updated successfully.')
        return redirect('suggestedJournals_view')
    else:
        messages.error(
            request, 'Error updating suggestedJournals  . Please check your input.')
        return redirect('suggestedJournals_view')


def update_suggestedSelfAwarnessBites(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'selfAwarnessBite': request.POST.get('selfAwarnessBite'),
            'state': request.POST.get('state'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),

        }
        db = firestore.client()
        db.collection("suggestedSelfAwarnessBites").document(
            entry_id).update(data)
        messages.success(
            request, 'suggestedSelfAwarnessBites updated successfully.')
        return redirect('suggestedSelfAwarnessBites_view')
    else:
        messages.error(
            request, 'Error updating  suggestedSelfAwarnessBites . Please check your input.')
        return redirect('suggestedSelfAwarnessBites_view')


def update_suggestedWildCards(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'wildCard': request.POST.get('wildCard'),
            'user': request.POST.get('user'),
            'time': request.POST.get('time'),

        }
        db = firestore.client()
        db.collection("suggestedWildCards").document(entry_id).update(data)
        messages.success(request, 'suggestedWildCards updated successfully.')
        return redirect('suggestedWildCards_view')
    else:
        messages.error(
            request, 'Error updating suggestedWildCards  . Please check your input.')
        return redirect('suggestedWildCards_view')


def update_testTrivia(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'answers': request.POST.get('answers'),
            'correct_answer': request.POST.get('correct_answer'),
            'correct_answer_index': request.POST.get('correct_answer_index'),
            'order': request.POST.get('order'),
            'question': request.POST.get('question'),

        }
        db = firestore.client()
        db.collection("testTrivia").document(entry_id).update(data)
        messages.success(request, 'testTrivia updated successfully.')
        return redirect('testTrivia_view')
    else:
        messages.error(
            request, 'Error updating testTrivia  . Please check your input.')
        return redirect('testTrivia_view')


def update_wildCard(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'content': request.POST.get('content'),
        }
        db = firestore.client()
        db.collection("wildCard").document(entry_id).update(data)
        messages.success(request, 'wildCard updated successfully.')
        return redirect('wildCard_view')
    else:
        messages.error(
            request, 'Error updating wildCard  . Please check your input.')
        return redirect('wildCard_view')


def update_selfladder(request, document_name):
    if request.method == 'POST':
        entry_id = document_name
        data = {
            'userID': request.POST.get('userID'),
            'type': request.POST.get('type'),
            'time': request.POST.get('time'),
        }
        db = firestore.client()
        db.collection("selfLadder").document(entry_id).update(data)
        messages.success(request, 'selfladder updated successfully.')
        return redirect('selfladder_view')
    else:
        messages.error(
            request, 'Error updating selfladder  . Please check your input.')
        return redirect('selfladder_view')


def patient_search(request):
    query = request.GET.get('q')
    if query:
        results = users.objects.filter(
            Q(display_name__icontains=query) | Q(email__icontains=query)
        )
    else:
        results = users.objects.none()

    return render(request, 'frontend/techcare_data/pations_search.html', {'results': results})

# def chartbiomarkers(request):
#     try:
#         # Fetch biomarkers data from Firestore
#         biomarkers_collection = db.collection("biomarkers")
#         biomarkers_documents = biomarkers_collection.stream()

#         # Prepare data for Chart.js
#         data_labels = []
#         data_values = []

#         for doc in biomarkers_documents:
#             # Ensure 'bloodGlucose' field exists in document
#             doc_data = doc.to_dict()
#             if 'time' in doc_data and 'bloodGlucose' in doc_data:
#                 timestamp = doc_data['time'].strftime("%Y-%m-%d %H:%M:%S")
#                 data_labels.append(timestamp)
#                 data_values.append(doc_data['bloodGlucose'])
#         # Prepare data in a format suitable for JavaScript (JSON)
#         data_for_chartjs = {
#             'labels': data_labels,
#             'datasets': [{
#                 'label': 'Blood Glucose Levels',
#                 'data': data_values,
#                 'borderColor': 'rgb(75, 192, 192)',
#                 'fill': False  # Line chart should not be filled
#             }]
#         }

#         return render(request, 'frontend/techcare_data/chart_biomarkers.html', {'data_for_chartjs': data_for_chartjs})

#     except Exception as e:
#         # Handle exceptions gracefully, e.g., log the error
#         import logging
#         logging.error(f"Error fetching biomarkers data: {str(e)}")
#         # Render an error page or return an HTTP response with error details
#         return render(request, 'error.html', {'error_message': str(e)})


def export_nutrition_data(request):
    # Fetch data from Firestore
    db = firestore.client()
    collection = db.collection("nutrition")
    documents = collection.stream()
    document_data = [{'name': doc.id, **doc.to_dict()} for doc in documents]

    # Create a new Excel workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Nutrition Data"

    # Define the column headers
    headers = [
        "carbContent", "name_ar", "name_en", "portion",
        "proteinContent", "totalCalories", "weight"
    ]
    worksheet.append(headers)

    # Add rows to the worksheet
    for entry in document_data:
        row = [
            entry.get("carbContent"),
            entry.get("name_ar"),
            entry.get("name_en"),
            entry.get("portion"),
            entry.get("proteinContent"),
            entry.get("totalCalories"),
            entry.get("weight")
        ]
        worksheet.append(row)

    # Save the workbook to a BytesIO stream
    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)

    # Create the HTTP response with the Excel file
    response = HttpResponse(
        stream.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="nutrition_data.xlsx"'
    return response



def import_nutrition_data(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        file = request.FILES['import_file']
        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            # Save the file temporarily
            file_name = default_storage.save(file.name, file)
            file_path = Path(settings.MEDIA_ROOT) / file_name

            # Process the file
            try:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(file_path)

                # Initialize Firestore client
                db = firestore.Client()

                # Reference to the Firestore collection
                collection_ref = db.collection("nutrition")

                # Add each row from the DataFrame to Firestore
                for index, row in df.iterrows():
                    document_data = {
                        "carbContent": row.get('carbContent'),
                        "name_ar": row.get('name_ar'),
                        "name_en": row.get('name_en'),
                        "portion": row.get('portion'),
                        "proteinContent": row.get('proteinContent'),
                        "totalCalories": row.get('totalCalories'),
                        "weight": row.get('weight')
                    }
                    # Add document to Firestore with auto-generated ID
                    collection_ref.add(document_data)

                messages.success(request, 'Data imported successfully!')
            except Exception as e:
                messages.error(request, f'Error importing data: {e}')
        else:
            messages.error(request, 'Invalid file format. Please upload an Excel file.')
        
        return redirect('nutrition_view')  # Redirect to the appropriate view

    return render(request, 'frontend/techcare_data/nutrition_table.html')
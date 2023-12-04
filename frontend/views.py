from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase import firebase
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from api.models import User
from frontend.forms import PatientForm, DoctorForm
from frontend.models import bites
import logging
from .forms import DocumentForm
from django.http import JsonResponse
from .models import collection

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
    db = firestore.Client()
    collection = db.collection("bites")
    documents = collection.stream()
    document_data = [{'name': doc.id, 'data': doc.to_dict()} for doc in documents]
    context = {'document_data': document_data}
    return render(request, 'frontend/techcare_data/bites_table.html', context)

def document_detail(request, document_name):
    db = firestore.Client()
    collection = db.collection("bites")
    document_ref = collection.document(document_name)
    document_data = document_ref.get().to_dict()

    if not document_data:
     
        return render(request, 'frontend/techcare_data/document_not_found.html')

    return render(request, 'frontend/techcare_data/document_detail.html', {'document_data': document_data})


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

def delete_document(request, document_id):
    if request.method == 'POST':
        db.collection('bites').document("vF6FnRYwG5tFGsBvMgYO").delete()
        return JsonResponse({'status': 'success', 'message': 'Document deleted successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def get_all_collections(request):
    db = firestore.client()
    all_collections = [collection.id for collection in db.collections()]
    
    return render(request, 'frontend/techcare_data/collections.html', {'collections': all_collections})

def handle_form_submission(request):
    if request.method == 'POST':
        selected_collection = request.POST.get('collection_dropdown')
        if selected_collection == 'bites':
            return redirect('bites_view')  
       ## elif 
        ##selected_collection == 'another_collection':
           ## return redirect('another_collection_view')  

    return render(request, 'frontend/techcare_data/collections.html')
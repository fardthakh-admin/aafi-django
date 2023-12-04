from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from .views import create_document, delete_document
from .views import get_all_collections, handle_form_submission
urlpatterns = [
    path('login', views.login_page, name="login"),
    path('logout/', views.logout_page, name='logout'),
    path('patient-signup/', views.patient_signup, name="patientSignup"),
    path('doctor-signup/', views.doctor_signup, name="doctorSignup"),

    path('patient-homepage/', views.patient_homepage, name="patient-homepage"),

    # DOCTOR PAGES
    path('doctor-homepage/', views.doctor_homepage, name="doctor-homepage"),
    path('doctor-patients/', views.patients_list, name="patients"),
    path('doctor-chat/', views.doctor_chat_page, name="doctor-chat"),

    path('calendar/', views.calendar, name="calendar"),
   # PATIENT PAGES
    path('patient-homepage/activities.html', views.mind_activities_view, name='mind_activities'),
    path('patient-homepage/quiz.html', views.quiz_question_view, name='quiz question'),
   # FIRESTORE PAGES
    path('bites_view/', views.bites_view, name='bites_view'),
    path('bites_table/', views.bites_view, name='bites_table'),
    path('document/<str:document_name>/', views.document_detail, name='document_detail'),
    path('create_document/', create_document, name='create_document'),
    path('delete_document/<str:document_id>/', views.delete_document, name='delete_document'),
    path('collections/', get_all_collections, name='collections'),
    path('handle_form_submission/', handle_form_submission, name='handle_form_submission'),
   
]

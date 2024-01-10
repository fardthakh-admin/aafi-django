from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from .views import create_document
from .views import get_all_collections, handle_form_submission
from.views import *

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
    path('activities_view/', views.activities_view, name='activities_view'),
    path('bites_table/', views.bites_view, name='bites_table'),
    path('document/bites/<str:document_name>/', views.bitesdocument_detail, name='bitesdocument'),
    path('document/activities/<str:document_name>/', views.activitiesdocument_detail, name='activitiesdocument'),
    path('document/categories/<str:document_name>/', views.categoriesdocument_detail, name='categoriesdocument'),
    path('document/feelings/<str:document_name>/', views.feelingsdocument_detail, name='feelingsdocument'),
    path('document/inAppLinks/<str:document_name>/', views.inAppLinksdocument_detail, name='inAppLinksdocument'),
    path('document/inquiry/<str:document_name>/', views.inquirydocument_detail, name='inquirydocument'),
    path('document/trivia/<str:document_name>/', views.triviadocument_detail, name='triviadocument'),
    path('document/items/<str:document_name>/', views.itemsdocument_detail, name='itemsdocument'),
    path('document/journal/<str:document_name>/', views.journaldocument_detail, name='journaldocument'),
    path('document/majorAssessment/<str:document_name>/', views.majorAssessmentdocument_detail, name='majorAssessmentdocument'),
    path('document/badges/<str:document_name>/', views.badgesdocument_detail, name='badgesdocument'),
    path('document/biomarkers/<str:document_name>/', views.biomarkersdocument_detail, name='biomarkersdocument'),
    path('document/scenarios/<str:document_name>/', views.scenariosdocument_detail, name='scenariosdocument'),
    path('document/shortBite/<str:document_name>/', views.shortBitedocument_detail, name='shortBitedocument'),
    path('document/tags/<str:document_name>/', views.tagsdocument_detail, name='tagsdocument'),
    path('document/users/<str:document_name>/', views.usersdocument_detail, name='usersdocument'),
    path('document/psychomarkers/<str:document_name>/', views.psychomarkersdocument_detail, name='psychomarkersdocument'),
    path('document/journalPrompt/<str:document_name>/', views.journalPromptdocument_detail, name='journalPromptdocument'),
    path('document/assessmentQuestion<str:document_name>/', views.assessmentQuestiondocument_detail, name='assessmentQuestiondocument'),
    path('create_document/', create_document, name='create_document'),
    path('create_tags/' , create_tags, name='create_tags'),
    path('collections/', get_all_collections, name='collections'),
    path('handle_form_submission/', handle_form_submission, name='handle_form_submission'),
    path('badges_view/', views.badges_view, name='badges_view'),
    path('biomarkers_view/', views.biomarkers_view, name='biomarkers_view'),
    path('assessmentQuestion_view/', views.assessmentQuestion_view, name='assessmentQuestion_view'),
    path('categories_view/', views.categories_view, name='categories_view'),
    path('feelings_view/', views.feelings_view, name='feelings_view'),
    path('inAppLinks_view/', views.inAppLinks_view, name='inAppLinks_view'),
    path('inquiry_view/', views.inquiry_view, name='inquiry_view'),
    path('items_view/', views.items_view, name='items_view'),
    path('journal_view/', views.journal_view, name='journal_view'),
    path('journalPrompt_view/', views.journalPrompt_view, name='journalPrompt_view'),
    path('majorAssessment_view/', views.majorAssessment_view, name='majorAssessment_view'),
    path('psychomarkers_view/', views.psychomarkers_view, name='psychomarkers_view'),
    path('scenarios_view/', views.scenarios_view, name='scenarios_view'),
    path('shortBite_view/', views.shortBite_view, name='shortBite_view'),
    path('tags_view/', views.tags_view, name='tags_view'),
    path('trivia_view/', views.trivia_view, name='trivia_view'),
    path('users_view/', views.users_view, name='users_view'),
    path('sidebar/', views.sidebar, name='sidebar'),
]

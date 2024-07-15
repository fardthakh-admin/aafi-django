from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.apiOverView, name="api-overview"),

    # Authentication and registration
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.UserLogin.as_view(), name = 'login'),



    path('logout/', views.LogoutUser.as_view(), name = 'logout'),

    # Users views
    path('user/', views.UserView.as_view(), name="user-view"),
    path('user-list/', views.UserList, name="user-list"),

    # Doctors list 
    path('doctor-list/', views.DoctorList, name="doctor-list"),
    path('doctor-detail/<str:pk>/', views.DoctorDetail, name="doctor-detail"),
    path('doctor-create/', views.DoctorCreate, name="doctor-create"),
    path('doctor-update/<str:pk>/', views.DoctorUpdate, name="doctor-update"),
    path('doctor-delete/<str:pk>/', views.DoctorDelete, name="doctor-delete"),

    # Patients List
    path('patient-list/', views.PatientList, name="patient-list"),
    path('patient-detail/<str:pk>/', views.PatientDetail, name="patient-detail"),
    path('patient-create/', views.PatientCreate, name="patient-create"),
    path('patient-delete/<str:pk>/', views.PatientDelete, name="patient-delete"),
    path('patient-update/<str:pk>/', views.PatientUpdate, name="patient-update"),
    path('patients/', views.Patients_Page, name="patients"),

    path('medication-list/', views.MedicationList, name="medication-list"),
    path('medication-detail/<str:pk>/', views.MedicationDetail, name="medication-detail"),
    path('medication-create/', views.MedicationCreate, name="medication-create"),
    path('medication-delete/<str:pk>/', views.MedicationDelete, name="medication-delete"),
    path('medication-update/<str:pk>/', views.MedicationUpdate, name="medication-update"),

    path('activity-list/', views.ActivityList, name="activity-list"),
    path('activity-detail/<str:pk>/', views.ActivityDetail, name="activity-detail"),
    path('activity-create/', views.ActivityCreate, name="activity-create"),
    path('activity-delete/<str:pk>/', views.ActivityDelete, name="activity-delete"),
    path('activity-update/<str:pk>/', views.ActivityUpdate, name="activity-update"),

    path('challenge-list/', views.ChallengeList, name="challenge-list"),
    path('challenge-detail/<str:pk>/', views.ChallengeDetail, name="challenge-detail"),
    path('challenge-create/', views.ChallengeCreate, name="challenge-create"),
    path('challenge-delete/<str:pk>/', views.ChallengeDelete, name="challenge-delete"),
    path('challenge-update/<str:pk>/', views.ChallengeUpdate, name="challenge-update"),

    path('message-list/', views.MessageList, name="message-list"),
    path('message-detail/<str:pk>/', views.MessageDetail, name="message-detail"),
    path('message-create/', views.MessageCreate, name="message-create"),
    path('message-delete/<str:pk>/', views.MessageDelete, name="message-delete"),
    path('message-update/<str:pk>/', views.MessageUpdate, name="message-update"),

    path('groups-list/', views.GroupsList, name="groups-list"),
    path('group-detail/<str:pk>/', views.GroupDetail, name="group-detail"),
    path('group-create/', views.GroupCreate, name="group-create"),
    path('group-delete/<str:pk>/', views.GroupDelete, name="group-delete"),
    path('group-update/<str:pk>/', views.GroupUpdate, name="group-update"),

    path('checkIn-list/', views.CheckInList, name="checkIn-list"),
    path('checkIn-detail/<str:pk>/', views.CheckInDetail, name="checkIn-detail"),
    path('checkIn-create/', views.CheckInCreate, name="checkIn-create"),
    path('checkIn-delete/<str:pk>/', views.CheckInDelete, name="checkIn-delete"),
    path('checkIn-update/<str:pk>/', views.CheckInUpdate, name="checkIn-update"),

    path('biomarkers-list/', views.BiomarkersList, name="biomarkers-list"),
    path('biomarkers-detail/<str:pk>/', views.BiomarkersDetail, name="biomarkers-detail"),
    path('biomarkers-create/', views.BiomarkersCreate, name="biomarkers-create"),
    path('biomarkers-delete/<str:pk>/', views.BiomarkersDelete, name="biomarkers-delete"),
    path('biomarkers-update/<str:pk>/', views.BiomarkerUpdate, name="biomarkers-update"),

    path('goal-list/', views.GoalList, name="goal-list"),
    path('goal-detail/<str:pk>/', views.GoalDetail, name="goal-detail"),
    path('goal-create/', views.GoalCreate, name="goal-create"),
    path('goal-delete/<str:pk>/', views.GoalDelete, name="goal-delete"),
    path('goal-update/<str:pk>/', views.GoalUpdate, name="goal-update"),

    path('badge-list/', views.BadgeList, name="badge-list"),
    path('badge-detail/<str:pk>/', views.BadgeDetail, name="badge-detail"),
    path('badge-create/', views.BadgeCreate, name="badge-create"),
    path('badge-delete/<str:pk>/', views.BadgeDelete, name="badge-delete"),
    path('badge-update/<str:pk>/', views.BadgeUpdate, name="badge-update"),

    path('CBT-list/', views.CBTList, name="CBT-list"),
    path('CBT-detail/<str:pk>/', views.CBTDetail, name="CBT-detail"),
    path('CBT-create/', views.CBTCreate, name="CBT-create"),
    path('CBT-delete/<str:pk>/', views.CBTDelete, name="CBT-delete"),
    path('CBT-update/<str:pk>/', views.CBTUpdate, name="CBT-update"),

    path('game-list/', views.GameList, name="game-list"),
    path('game-detail/<str:pk>/', views.GameDetail, name="game-detail"),
    path('game-create/', views.GameCreate, name="game-create"),
    path('game-delete/<str:pk>/', views.GameDelete, name="game-delete"),
    path('game-update/<str:pk>/', views.GameUpdate, name="game-update"),

    path('evaluation-list/', views.EvaluationList, name="evaluation-list"),
    path('evaluation-detail/<str:pk>/', views.EvaluationDetail, name="evaluation-detail"),
    path('evaluation-create/', views.EvaluationCreate, name="evaluation-create"),
    path('evaluation-delete/<str:pk>/', views.EvaluationDelete, name="evaluation-delete"),
    path('evaluation-update/<str:pk>/', views.EvaluationUpdate, name="evaluation-update"),

    path('question-list/', views.QuestionList, name="question-list"),
    path('question-detail/<str:pk>/', views.QuestionDetail, name="question-detail"),
    path('question-create/', views.QuestionCreate, name="question-create"),
    path('question-delete/<str:pk>/', views.QuestionDelete, name="question-delete"),
    path('question-update/<str:pk>/', views.QuestionUpdate, name="question-update"),

    path('historicalDiagnosis-list/', views.HistoricalDiagnosisList, name="historicalDiagnosis-list"),
    path('historicalDiagnosis-detail/<str:pk>/', views.HistoricalDiagnosisDetail, name="historicalDiagnosis-detail"),
    path('historicalDiagnosis-create/', views.HistoricalDiagnosisCreate, name="historicalDiagnosis-create"),
    path('historicalDiagnosis-delete/<str:pk>/', views.HistoricalDiagnosisDelete, name="historicalDiagnosis-delete"),
    path('historicalDiagnosis-update/<str:pk>/', views.HistoricalDiagnosisUpdate, name="historicalDiagnosis-update"),
    path('biomarker-chart/', views.BiomarkersChart, name="biomarker-chart"), 

    path('unit-list/', views.UnitList, name="unit-list"),
    path('unit-create/', views.UnitCreate, name="unit-create"),
    path('unit-update/<str:pk>/', views.UnitUpdate, name="unit-update"),
    path('unit-delete/<str:pk>/', views.UnitDelete, name="unit-delete"),
    path('unit-detail/<str:pk>/', views.UnitDetail, name="unit-detail"),

    



    




]

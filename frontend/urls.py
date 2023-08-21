from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name="login"),
    path('patient-signup/', views.patient_signup, name="patientSignup"),
    path('doctor-signup/', views.doctor_signup, name="doctorSignup"),

    path('patient-homepage/', views.patient_homepage, name="patient-homepage"),

    # DOCTOR PAGES
    path('doctor-homepage/', views.doctor_homepage, name="doctor-homepage"),
    path('patients/', views.patients_list, name="patients"),

    path('calendar/', views.calendar, name="calendar"),

]

from django.urls import path
from . import views
# from .views import

urlpatterns = [
    path('', views.login_page, name="login"),
    path('patient-signup/', views.patient_signup, name="patientSignup"),
    path('doctor-signup/', views.doctor_signup, name="doctorSignup"),

    path('patient/patient-homepage/', views.patient_homepage, name="patient-homepage"),
    path('doctor/doctor-homepage/', views.doctor_homepage, name="doctor-homepage"),

]

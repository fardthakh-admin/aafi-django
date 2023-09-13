from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
#as_view(template_name="login_signup.html")
urlpatterns = [
    path('login', views.login_page, name="login"),
    path('patient-signup/', views.patient_signup, name="patientSignup"),
    path('doctor-signup/', views.doctor_signup, name="doctorSignup"),

    path('patient-homepage/', views.patient_homepage, name="patient-homepage"),

    # DOCTOR PAGES
    path('doctor-homepage/', views.doctor_homepage, name="doctor-homepage"),
    path('doctor-patients/', views.patients_list, name="patients"),
    path('doctor-chat/', views.doctor_chat_page, name="doctor-chat"),

    path('calendar/', views.calendar, name="calendar"),

]

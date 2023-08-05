from django.urls import path
from . import views
# from .views import

urlpatterns = [
    path('', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('patientSignup/', views.patient_signup, name="patientSignup"),
    path('doctorSignup/', views.doctor_signup, name="doctorSignup"),

    path('patient/patientHomepage/', views.patient_homepage, name="patientHomepage"),
    path('doctor/doctorHomepage/', views.doctor_homepage, name="doctorHomepage"),

]

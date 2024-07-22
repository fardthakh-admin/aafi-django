from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from .views import create_document
from .views import get_all_collections, handle_form_submission
from.views import *
from .views import admin_required

urlpatterns = [

    path('patient-homepage/', views.patient_homepage, name="patient-homepage"),

    # DOCTOR PAGES
    path('doctor-homepage/', views.doctor_homepage, name="doctor-homepage"),
    path('doctor-patients/', views.patients_list, name="patients"),
    path('doctor-chat/', views.doctor_chat_page, name="doctor-chat"),
    
    path('doctor-patients/search/', patient_search, name='patient-search'),

    path('calendar/', views.calendar, name="calendar"),
   # PATIENT PAGES
    path('patient-homepage/activities.html', views.mind_activities_view, name='mind_activities'),
    path('patient-homepage/quiz.html', views.quiz_question_view, name='quiz question'),
   # FIRESTORE PAGES
    path('bites_view/', views.bites_view, name='bites_view'),
    path('activities_view/', views.activities_view, name='activities_view'),
    path('assets_view/', views.assets_view, name='assets_view'),
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
    path('document/assessmentQuestion/<str:document_name>/', views.assessmentQuestiondocument_detail, name='assessmentQuestiondocument'),
    path('document/patients/<str:document_name>/', views.patients_detail, name='patientsdocument'),
    path('create_document/', create_document, name='create_document'),
    path('create_activities/',create_activities, name='create_activities'),
    path('create_assets/', create_assets, name='create_assets'),

    path('create_assessmentQuestion/', create_assessmentQuestion, name='create_assessmentQuestion'),
    path('create_badges/', create_badges,  name='create_badges'),
    path('create_biomarkers/', create_biomarkers,  name='create_biomarkers'),
    path('create_categories/', create_categories,  name='create_categories'),
    path('create_shortBite/', create_shortBite,  name='create_shortBite'),
    path('create_feelings/', create_feelings, name='create_feelings'),
    path('create_inAppLinks/', create_inAppLinks, name='create_inAppLinks'),
    path('create_inquiry/',create_inquiry, name='create_inquiry'),
    path('create_items/', create_items, name='create_items'),
    path('create_journal/',create_journal, name='create_journal'),
    path('create_journalPrompt/', create_journalPrompt,  name='create_journalPrompt'),
    path('create_majorAssessment/', create_majorAssessment,  name='create_majorAssessment'),
    path('create_psychomarkers/', create_psychomarkers,  name='create_psychomarkers'),
    path('create_scenarios/', create_scenarios,  name='create_scenarios'),
    path('create_selfawarenessScenarios/', create_selfAwarenessScenarios,  name='create_selfAwarenessScenarios'),
    path('create_selfLadder/', create_selfLadder,  name='create_selfLadder'),
    path('create_selfAwarnessBites/', create_selfAwarnessBites,  name='create_selfAwarnessBites'),
    path('create_wildCard/', create_wildCard,  name='create_wildCard'),


    


    path('create_tags/', create_tags,  name='create_tags'),
    path('create_trivia/', create_trivia,  name='create_trivia'),
    path('create_users/', create_users, name='create_users'),
    path('create_nutrition/', create_nutrition, name='create_nutrition'),


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

    path('selfawarenessScenarios_view/', views.selfawarenessScenarios_view, name='selfawarenessScenarios_view'), 
    path('assets_view/', views.assets_view, name='assets_view'),
    path('nutrition_view/', views.nutrition_view, name='nutrition_view'),
    path('readBites_view/', views.readBites_view, name='readBites_view'),
    path('readStories_view/', views.readStories_view, name='readStories_view'),
    path('selfAwarnessBites_view/', views.selfAwarnessBites_view, name='selfAwarnessBites_view'),
    path('selfawareness_collection_view/', views.selfawareness_collection_view, name='selfawareness_collection_view'),
    path('suggestedActivities_view/', views.suggestedActivities_view, name='suggestedActivities_view'),
    path('suggestedBites_view/', views.suggestedBites_view, name='suggestedBites_view'),
    path('suggestedInAppLinks_view/', views.suggestedInAppLinks_view, name='suggestedInAppLinks_view'),
    path('suggestedJournals_view/', views.suggestedJournals_view, name='suggestedJournals_view'),
    path('suggestedSelfAwarnessBites_view/', views.suggestedSelfAwarnessBites_view, name='suggestedSelfAwarnessBites_view'),
    path('suggestedWildCards_view/', views.suggestedWildCards_view, name='suggestedWildCards_view'),
    path('testTrivia_view/', views.testTrivia_view, name='testTrivia_view'),
    path('wildCard_view/', views.wildCard_view, name='wildCard_view'),
    path('selfladder_view/', views.selfladder_view, name='selfladder_view'),

    path('sidebar/', views.sidebar, name='sidebar'),


    path('activities/delete/<str:document_name>/', views.activities_delete, name='activities_delete'),
    path('assessmentQuestion/delete/<str:document_name>/', views.assessmentQuestion_delete, name='assessmentQuestion_delete'),
    path('assets/delete/<str:document_name>/', views.assets_delete, name='assets_delete'),

    path('badges/delete/<str:document_name>/', views.badges_delete, name='badges_delete'),
    path('biomarkers/delete/<str:document_name>/', views.biomarkers_delete, name='biomarkers_delete'),
    path('bites/delete/<str:document_name>/', views.bites_delete, name='bites_delete'),
    path('categories/delete/<str:document_name>/', views.categories_delete, name='categories_delete'),
    path('feelings/delete/<str:document_name>/', views.feelings_delete, name='feelings_delete'),
    path('inAppLinks/delete/<str:document_name>/', views.inAppLinks_delete, name='inAppLinks_delete'),
    path('inquiry/delete/<str:document_name>/', views.inquiry_delete, name='inquiry_delete'),
    path('items/delete/<str:document_name>/', views.items_delete, name='items_delete'),
    path('journal/delete/<str:document_name>/', views.journal_delete, name='journal_delete'),
    path('journalPrompt/delete/<str:document_name>/', views.journalPrompt_delete, name='journalPrompt_delete'),
    path('majorAssessment/delete/<str:document_name>/', views.majorAssessment_delete, name='majorAssessment_delete'),
    path('psychomarkers/delete/<str:document_name>/', views.psychomarkers_delete, name='psychomarkers_delete'),
    path('scenarios/delete/<str:document_name>/', views.scenarios_delete, name='scenarios_delete'),
    path('shortBite/delete/<str:document_name>/', views.shortBite_delete, name='shortBite_delete'),
    path('tags/delete/<str:document_name>/', views.tags_delete, name='tags_delete'),
    path('trivia/delete/<str:document_name>/', views.trivia_delete, name='trivia_delete'),
    path('users/delete/<str:document_name>/', views.users_delete, name='users_delete'),

    path('selfawarenessBites/delete/<str:document_name>/', views.selfawarenessBites_delete, name='selfawarenessBites_delete'),
    path('selfawarenessCollection/delete/<str:document_name>/', views.selfawarenessCollection_delete, name='selfawarenessCollection_delete'),
    path('selfLadder/delete/<str:document_name>/', views.selfLadder_delete, name='selfLadder_delete'),
    path('selfawarenessScenarios/delete/<str:document_name>/', views.selfawarenessScenarios_delete, name='selfawarenessScenarios_delete'),
    path('selfLadder/delete/<str:document_name>/', views.selfLadder_delete, name='selfLadder_delete'),
    path('wildCard/delete/<str:document_name>/', views.wildCard_delete, name='wildCard_delete'),
    # path('/delete/<str:document_name>/', views._delete, name='_delete'),

    path('update/activities/<str:document_name>', update_activities, name='update_activities'),
    path('update/assessmentQuestion/<str:document_name>', update_assessmentQuestion, name='update_assessmentQuestion'),
    path('update/badges/<str:document_name>', update_badges, name='update_badges'),
    path('update/biomarkers/<str:document_name>', update_biomarkers, name='update_biomarkers'),
    path('update/bites/<str:document_name>', update_bites, name='update_bites'),
    path('update/categories/<str:document_name>', update_categories, name='update_categories'),
    path('update/feelings/<str:document_name>', update_feelings, name='update_feelings'),
    path('update/inAppLinks/<str:document_name>', update_inAppLinks, name='update_inAppLinks'),
    path('update/inquiry/<str:document_name>', update_inquiry, name='update_inquiry'),
    path('update/items/<str:document_name>', update_items, name='update_items'),
    path('update/journal/<str:document_name>', update_journal, name='update_journal'),
    path('update/journalPrompt/<str:document_name>', update_journalPrompt, name='update_journalPrompt'),
    path('update/majorAssessment/<str:document_name>', update_majorAssessment, name='update_majorAssessment'),
    path('update/psychomarkers/<str:document_name>', update_psychomarkers, name='update_psychomarkers'),
    path('update/scenarios/<str:document_name>', update_scenarios, name='update_scenarios'),
    path('update/shortBite/<str:document_name>', update_shortBite, name='update_shortBite'),
    path('update/tags/<str:document_name>', update_tags, name='update_tags'),
    path('update/trivia/<str:document_name>', update_trivia, name='update_trivia'),
    path('update/users/<str:document_name>', update_users, name='update_users'),

    path('update/selfawarenessScenarios/<str:document_name>', update_selfawarenessScenarios, name='update_selfawarenessScenarios'),

    path('update/assets/<str:document_name>', update_assets, name='update_assets'),
    path('update/nutrition/<str:document_name>', update_nutrition, name='update_nutrition'),
    path('update/readBites/<str:document_name>', update_readBites, name='update_readBites'),
    path('update/readStories/<str:document_name>', update_readStories, name='update_readStories'),
    path('update/selfAwarnessBites/<str:document_name>', update_selfAwarnessBites, name='update_selfAwarnessBites'),
    path('update/selfawareness_collection/<str:document_name>', update_selfawareness_collection, name='update_selfawareness_collection'),
    path('update/suggestedActivities/<str:document_name>', update_suggestedActivities, name='update_suggestedActivities'),
    path('update/suggestedBites/<str:document_name>', update_suggestedBites, name='update_suggestedBites'),
    path('update/suggestedInAppLinks/<str:document_name>', update_suggestedInAppLinks, name='update_suggestedInAppLinks'),
    path('update/suggestedJournals/<str:document_name>', update_suggestedJournals, name='update_suggestedJournals'),
    path('update/suggestedSelfAwarnessBites/<str:document_name>',update_suggestedSelfAwarnessBites, name='update_suggestedSelfAwarnessBites'),
    path('update/suggestedWildCards/<str:document_name>', update_suggestedWildCards, name='update_suggestedWildCards'),
    path('update/testTrivia/<str:document_name>', update_testTrivia, name='update_testTrivia'),
    path('update/wildCard/<str:document_name>', update_wildCard, name='update_wildCard'),
    path('update/selfladder/<str:document_name>', update_selfladder, name='update_selfladder'),
    # path('update//<str:document_name>', update_, name='update_'),
    

    # path('chart/biomarkers', views.chartbiomarkers, name="chartbiomarkers"),

  


]

for pattern in urlpatterns:
    if hasattr(pattern, 'callback') and hasattr(pattern.callback, '__name__'):
        pattern.callback = admin_required(pattern.callback)

urlpatterns += [
    path('', views.login_page),
    path('login', views.login_page, name="login"),
    path('logout/', views.logout_page, name='logout'),
    path('patient-signup/', views.patient_signup, name="patientSignup"),
    path('doctor-signup/', views.doctor_signup, name="doctorSignup"),
]

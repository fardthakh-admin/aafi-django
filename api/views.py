from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import *
from .models import *

import jwt, datetime

@api_view(['GET'])
def apiOverView(request):
    api_urls = {
        'register_user': '/register/',
        'login_user': '/login/',
        'logout_user': '/logout/',

        'Doctors': '/doctor-list/',
        'Doctor_Detail_View': '/doctor-detail/<str:pk>/',
        'Doctor_Create': '/doctor-create/',
        'Doctor_Delete': '/doctor-delete/<str:pk>/',
        'Doctor_Update': '/doctor-update/<str:pk>/',
        'Patients_Page': '/patients/',


        'Patients': '/patient-list/',
        'Patient Detail View': '/patient-detail/<str:pk>/',
        'Patient Create': '/patient-create/',
        'Patient Delete': '/patient-delete/<str:pk>/',
        'Patient Update': '/patient-update/<str:pk>/',

        'Medication': '/medication-list/',
        'Medication Detail View': '/medication-detail/<str:pk>/',
        'Medication Create': '/medication-create/',
        'Medication Delete': '/medication-delete/<str:pk>/',
        'Medication Update': '/medication-update/<str:pk>/',

        'Activity': '/activity-list/',
        'Activity Detail View': '/challenge-detail/<str:pk>/',
        'Activity Create': '/activity-create/',
        'Activity Delete': '/activity-delete/<str:pk>/',
        'Activity Update': '/activity-update/<str:pk>/',

        'Challenge': '/challenge-list/',
        'Challenge Detail View': '/challenge-detail/<str:pk>/',
        'Challenge Create': '/challenge-create/',
        'Challenge Delete': '/challenge-delete/<str:pk>/',
        'Challenge Update': '/challenge-update/<str:pk>/',

        'Message': '/message-list/',
        'Message Detail View': '/message-detail/<str:pk>/',
        'Message Create': '/message-create/',
        'Message Delete': '/message-delete/<str:pk>/',
        'Message Update': '/message-update/<str:pk>/',

        'Groups': '/groups-list/',
        'Group Detail View': '/group-detail/<str:pk>/',
        'Group Create': '/group-create/',
        'Group Delete': '/group-delete/<str:pk>/',
        'Group Update': '/group-update/<str:pk>/',

        'CheckIn': '/checkIn-list/',
        'CheckIn Detail View': '/checkIn-detail/<str:pk>/',
        'CheckIn Create': '/checkIn-create/',
        'CheckIn Delete': '/checkIn-delete/<str:pk>/',
        'CheckIn Update': '/checkIn-update/<str:pk>/',

        'Biomarkers': '/biomarkers-list/',
        'Biomarkers Detail View': '/biomarkers-detail/<str:pk>/',
        'Biomarkers Create': '/biomarkers-create/',
        'Biomarkers Delete': '/biomarkers-delete/<str:pk>/',
        'Biomarkers Update': '/biomarkers-update/<str:pk>/',

        'Goal': '/goal-list/',
        'Goal Detail View': '/goal-detail/<str:pk>/',
        'Goal Create': '/goal-create/',
        'Goal Delete': '/goal-delete/<str:pk>/',
        'Goal Update': '/goal-update/<str:pk>/',

        'Badge': '/badge-list/',
        'Badge Detail View': '/badge-detail/<str:pk>/',
        'Badge Create': '/badge-create/',
        'Badge Delete': '/badge-delete/<str:pk>/',
        'Badge Update': '/badge-update/<str:pk>/',

        'CBT': '/CBT-list/',
        'CBT Detail View': '/CBT-detail/<str:pk>/',
        'CBT Create': '/CBT-create/',
        'CBT Delete': '/CBT-delete/<str:pk>/',
        'CBT Update': '/CBT-update/<str:pk>/',

        'Game': '/game-list/',
        'Game Detail View': '/game-detail/<str:pk>/',
        'Game Create': '/game-create/',
        'Game Delete': '/game-delete/<str:pk>/',
        'Game Update': '/game-update/<str:pk>/',

        'Evaluation': '/evaluation-list/',
        'Evaluation Detail View': '/evaluation-detail/<str:pk>/',
        'Evaluation Create': '/evaluation-create/',
        'Evaluation Delete': '/evaluation-delete/<str:pk>/',
        'Evaluation Update': '/evaluation-update/<str:pk>/',

        'Question': '/question-list/',
        'Question Detail View': '/question-detail/<str:pk>/',
        'Question Create': '/question-create/',
        'Question Delete': '/question-delete/<str:pk>/',
        'Question Update': '/question-update/<str:pk>/',

        'HistoricalDiagnosis': '/historicalDiagnosis-list/',
        'HistoricalDiagnosis Detail View': '/historicalDiagnosis-detail/<str:pk>/',
        'HistoricalDiagnosis Create': '/historicalDiagnosis-create/',
        'HistoricalDiagnosis Delete': '/historicalDiagnosis-delete/<str:pk>/',
        'HistoricalDiagnosis Update': '/historicalDiagnosis-update/<str:pk>/',

    }
    return Response(api_urls)


# AUTHENTICATION VIEWS
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response(serializer.data)


class UserLogin(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.get(username = username)

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm = 'HS256')

        response = Response()

        response.set_cookie(key = 'jwt', value = token, httponly = True) # httponly means we dont want the frontend to access the token
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.get(id = payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutUser(APIView):
    def post(self, request):
        response = Response()
        
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Success!'
        }

        return response


@api_view(['GET'])
def UserList(request):
    user = User.objects.all()
    serializer = DoctorSerializer(user, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def DoctorList(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def DoctorDetail(request, pk):
    doctors = Doctor.objects.get(id = pk)
    serializer = DoctorSerializer(doctors, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def DoctorCreate(request):
    serializer = DoctorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def DoctorUpdate(request, pk):
    doctor = Doctor.objects.get(id=pk)
    serializer = DoctorSerializer(instance=doctor, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def DoctorDelete(request, pk):
    doctor = Doctor.objects.get(id=pk)
    doctor.delete()

    return Response('Item successfully deleted!')


@api_view(['GET'])
def Patients_Page(request):
    user = User.objects.get(id = request.user.id)
    patients = Patient.objects.filter(my_doctor = user)
    serializer = PatientPageListSerializer(patients, many=True)

    return Response(serializer.data)
    



@api_view(['GET'])
def PatientList(request):
    user = User.objects.get(id = request.user.id)
    patients = Patient.objects.filter(my_doctor = user)
    serializer = PatientSerializer(patients, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def PatientDetail(request, pk):
    patients = Patient.objects.get(id=pk)
    serializer = PatientSerializer(patients, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def PatientCreate(request):
    serializer = PatientSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def PatientDelete(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def PatientUpdate(request, pk):
    patient = Patient.objects.get(id=pk)
    serializer = PatientSerializer(instance=patient, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def MedicationList(request):
    medications = Medication.objects.all()
    serializer = MedicationSerializer(medications, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def MedicationDetail(request, pk):
    medications = Medication.objects.get(id=pk)
    serializer = MedicationSerializer(medications, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def MedicationCreate(request):
    serializer = MedicationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def MedicationDelete(request, pk):
    medication = Medication.objects.get(id=pk)
    medication.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def MedicationUpdate(request, pk):
    medication = Medication.objects.get(id=pk)
    serializer = MedicationSerializer(instance=medication, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def ActivityList(request):
    activities = Medication.objects.all()
    serializer = ActivitySerializer(activities, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def ActivityDetail(request, pk):
    activities = Activity.objects.get(id=pk)
    serializer = ActivitySerializer(activities, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def ActivityCreate(request):
    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def ActivityDelete(request, pk):
    activity = Activity.objects.get(id=pk)
    activity.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def ActivityUpdate(request, pk):
    activity = Activity.objects.get(id=pk)
    serializer = ActivitySerializer(instance=activity, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def ChallengeList(request):
    challenges = Medication.objects.all()
    serializer = ChallengeSerializer(challenges, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def ChallengeDetail(request, pk):
    challenges = Challenge.objects.get(id=pk)
    serializer = ChallengeSerializer(challenges, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def ChallengeCreate(request):
    serializer = ChallengeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def ChallengeDelete(request, pk):
    challenge = Challenge.objects.get(id=pk)
    challenge.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def ChallengeUpdate(request, pk):
    challenge = Challenge.objects.get(id=pk)
    serializer = ChallengeSerializer(instance=challenge, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def MessageList(request):
    messages = Medication.objects.all()
    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def MessageDetail(request, pk):
    messages = Message.objects.get(id=pk)
    serializer = MessageSerializer(messages, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def MessageCreate(request):
    serializer = MessageSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def MessageDelete(request, pk):
    message = Message.objects.get(id=pk)
    message.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def MessageUpdate(request, pk):
    message = Message.objects.get(id=pk)
    serializer = MessageSerializer(instance=message, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def GroupsList(request):
    groups = Groups.objects.all()
    serializer = GroupsSerializer(groups, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def GroupDetail(request, pk):
    group = Groups.objects.get(id=pk)
    serializer = GroupsSerializer(group, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def GroupCreate(request):
    serializer = GroupsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def GroupDelete(request, pk):
    group = Groups.objects.get(id=pk)
    group.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def GroupUpdate(request, pk):
    group = Groups.objects.get(id=pk)
    serializer = GroupsSerializer(instance=group, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def CheckInList(request):
    checkIns = CheckIn.objects.all()
    serializer = CheckInSerializer(checkIns, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def CheckInDetail(request, pk):
    checkIns = CheckIn.objects.get(id=pk)
    serializer = CheckInSerializer(checkIns, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def CheckInCreate(request):
    serializer = CheckInSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def CheckInDelete(request, pk):
    checkIn = CheckIn.objects.get(id=pk)
    checkIn.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def CheckInUpdate(request, pk):
    checkIn = CheckIn.objects.get(id=pk)
    serializer = CheckInSerializer(instance=checkIn, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def BiomarkersList(request):
    biomarkers = Biomarkers.objects.all()
    serializer = BiomarkersSerializer(biomarkers, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def BiomarkersDetail(request, pk):
    biomarkers = Biomarkers.objects.get(id=pk)
    serializer = BiomarkersSerializer(biomarkers, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def BiomarkersCreate(request):
    serializer = BiomarkersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def BiomarkersDelete(request, pk):
    biomarker = Biomarkers.objects.get(id=pk)
    biomarker.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def BiomarkerUpdate(request, pk):
    biomarker = Biomarkers.objects.get(id=pk)
    serializer = BiomarkersSerializer(instance=biomarker, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def GoalList(request):
    goals = Goal.objects.all()
    serializer = GoalSerializer(goals, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def GoalDetail(request, pk):
    goal = Goal.objects.get(id=pk)
    serializer = GoalSerializer(goal, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def GoalCreate(request):
    serializer = GoalSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def GoalDelete(request, pk):
    goal = Goal.objects.get(id=pk)
    goal.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def GoalUpdate(request, pk):
    goal = Goal.objects.get(id=pk)
    serializer = GoalSerializer(instance=goal, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def BadgeList(request):
    badges = Badge.objects.all()
    serializer = BadgeSerializer(badges, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def BadgeDetail(request, pk):
    badge = Badge.objects.get(id=pk)
    serializer = BadgeSerializer(badge, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def BadgeCreate(request):
    serializer = BadgeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def BadgeDelete(request, pk):
    badge = Badge.objects.get(id=pk)
    badge.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def BadgeUpdate(request, pk):
    badge = Badge.objects.get(id=pk)
    serializer = BadgeSerializer(instance=badge, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def CBTList(request):
    cbt = CBT.objects.all()
    serializer = CBTSerializer(cbt, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def CBTDetail(request, pk):
    cbt = CBT.objects.get(id=pk)
    serializer = CBTSerializer(cbt, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def CBTCreate(request):
    serializer = CBTSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def CBTDelete(request, pk):
    cbt = CBT.objects.get(id=pk)
    cbt.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def CBTUpdate(request, pk):
    cbt = CBT.objects.get(id=pk)
    serializer = CBTSerializer(instance=cbt, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def GameList(request):
    game = Game.objects.all()
    serializer = GameSerializer(game, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def GameDetail(request, pk):
    game = Game.objects.get(id=pk)
    serializer = GameSerializer(game, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def GameCreate(request):
    serializer = GameSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def GameDelete(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def GameUpdate(request, pk):
    game = Game.objects.get(id=pk)
    serializer = GameSerializer(instance=game, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def EvaluationList(request):
    evaluations = Evaluation.objects.all()
    serializer = EvaluationSerializer(evaluations, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def EvaluationDetail(request, pk):
    evaluation = Evaluation.objects.get(id=pk)
    serializer = EvaluationSerializer(evaluation, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def EvaluationCreate(request):
    serializer = EvaluationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def EvaluationDelete(request, pk):
    evaluation = Evaluation.objects.get(id=pk)
    evaluation.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def EvaluationUpdate(request, pk):
    evaluation = Evaluation.objects.get(id=pk)
    serializer = EvaluationSerializer(instance=evaluation, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def QuestionList(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def QuestionDetail(request, pk):
    question = Question.objects.get(id=pk)
    serializer = EvaluationSerializer(question, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def QuestionCreate(request):
    serializer = QuestionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def QuestionDelete(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def QuestionUpdate(request, pk):
    question = Question.objects.get(id=pk)
    serializer = QuestionSerializer(instance=question, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def HistoricalDiagnosisList(request):
    historicalDiagnosis = HistoricalDiagnosis.objects.all()
    serializer = HistoricalDiagnosisSerializer(historicalDiagnosis, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def HistoricalDiagnosisDetail(request, pk):
    historicalDiagnosis = HistoricalDiagnosis.objects.get(id=pk)
    serializer = HistoricalDiagnosisSerializer(historicalDiagnosis, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def HistoricalDiagnosisCreate(request):
    serializer = HistoricalDiagnosisSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def HistoricalDiagnosisDelete(request, pk):
    historicalDiagnosis = HistoricalDiagnosis.objects.get(id=pk)
    historicalDiagnosis.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
def HistoricalDiagnosisUpdate(request, pk):
    historicalDiagnosis = HistoricalDiagnosis.objects.get(id=pk)
    serializer = HistoricalDiagnosisSerializer(instance=historicalDiagnosis, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

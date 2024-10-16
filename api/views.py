from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from .serializers import *
from .models import *
import jwt
from datetime import datetime, timedelta
from firebase_admin import firestore
from functools import wraps
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import firebase_admin

from dateutil import parser
from dateutil import parser as date_parser

def jwt_login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Decode token and retrieve user data
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])

            # Check if user is superuser or staff
            if not user.is_superuser and not user.is_staff:
                raise AuthenticationFailed('Unauthorized! User must be superuser or staff.')

            request.user = user  # Set the user object in request for further use

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token. Please log in again.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        return view_func(request, *args, **kwargs)

    return wrapped_view

@api_view(['GET'])
@jwt_login_required
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

        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

    
User = get_user_model()




class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')        
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
@jwt_login_required
def UserList(request):
    user = User.objects.all()
    serializer = DoctorSerializer(user, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def DoctorList(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def DoctorDetail(request, pk):
    doctors = Doctor.objects.get(id = pk)
    serializer = DoctorSerializer(doctors, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def DoctorCreate(request):
    serializer = DoctorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def DoctorUpdate(request, pk):
    doctor = Doctor.objects.get(id=pk)
    serializer = DoctorSerializer(instance=doctor, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def DoctorDelete(request, pk):
    doctor = Doctor.objects.get(id=pk)
    doctor.delete()

    return Response('Item successfully deleted!')


@api_view(['GET'])
@jwt_login_required
def Patients_Page(request):
    user = User.objects.get(id = request.user.id)
    patients = Patient.objects.filter(my_doctor = user)
    serializer = PatientPageListSerializer(patients, many=True)

    return Response(serializer.data)
    



@api_view(['GET'])
@jwt_login_required
def PatientList(request):
    user = User.objects.get(id = request.user.id)
    patients = Patient.objects.filter(my_doctor = user)
    serializer = PatientSerializer(patients, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def PatientDetail(request, pk):
    patients = Patient.objects.get(id=pk)
    serializer = PatientSerializer(patients, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def PatientCreate(request):
    serializer = PatientSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def PatientDelete(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def PatientUpdate(request, pk):
    patient = Patient.objects.get(id=pk)
    serializer = PatientSerializer(instance=patient, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def MedicationList(request):
    medications = Medication.objects.all()
    serializer = MedicationSerializer(medications, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def MedicationDetail(request, pk):
    medications = Medication.objects.get(id=pk)
    serializer = MedicationSerializer(medications, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def MedicationCreate(request):
    serializer = MedicationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def MedicationDelete(request, pk):
    medication = Medication.objects.get(id=pk)
    medication.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def MedicationUpdate(request, pk):
    medication = Medication.objects.get(id=pk)
    serializer = MedicationSerializer(instance=medication, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def ActivityList(request):
    activities = Medication.objects.all()
    serializer = ActivitySerializer(activities, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def ActivityDetail(request, pk):
    activities = Activity.objects.get(id=pk)
    serializer = ActivitySerializer(activities, many=False)

    return Response(serializer.data)



@api_view(['GET'])
@jwt_login_required
def ActivityList(request):
    activities = Medication.objects.all()
    serializer = ActivitySerializer(activities, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def ActivityDetail(request, pk):
    activities = Activity.objects.get(id=pk)
    serializer = ActivitySerializer(activities, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def ActivityCreate(request):
    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def ActivityDelete(request, pk):
    activity = Activity.objects.get(id=pk)
    activity.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@api_view(['POST'])
@jwt_login_required
def ActivityCreate(request):
    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def ActivityDelete(request, pk):
    activity = Activity.objects.get(id=pk)
    activity.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def ActivityUpdate(request, pk):
    activity = Activity.objects.get(id=pk)
    serializer = ActivitySerializer(instance=activity, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def ChallengeList(request):
    challenges = Medication.objects.all()
    serializer = ChallengeSerializer(challenges, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def ChallengeDetail(request, pk):
    challenges = Challenge.objects.get(id=pk)
    serializer = ChallengeSerializer(challenges, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def ChallengeCreate(request):
    serializer = ChallengeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def ChallengeDelete(request, pk):
    challenge = Challenge.objects.get(id=pk)
    challenge.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def ChallengeUpdate(request, pk):
    challenge = Challenge.objects.get(id=pk)
    serializer = ChallengeSerializer(instance=challenge, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def MessageList(request):
    messages = Medication.objects.all()
    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def MessageDetail(request, pk):
    messages = Message.objects.get(id=pk)
    serializer = MessageSerializer(messages, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def MessageCreate(request):
    serializer = MessageSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def MessageDelete(request, pk):
    message = Message.objects.get(id=pk)
    message.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def MessageUpdate(request, pk):
    message = Message.objects.get(id=pk)
    serializer = MessageSerializer(instance=message, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def GroupsList(request):
    groups = Groups.objects.all()
    serializer = GroupsSerializer(groups, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def GroupDetail(request, pk):
    group = Groups.objects.get(id=pk)
    serializer = GroupsSerializer(group, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def GroupCreate(request):
    serializer = GroupsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def GroupDelete(request, pk):
    group = Groups.objects.get(id=pk)
    group.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def GroupUpdate(request, pk):
    group = Groups.objects.get(id=pk)
    serializer = GroupsSerializer(instance=group, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def CheckInList(request):
    checkIns = CheckIn.objects.all()
    serializer = CheckInSerializer(checkIns, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def CheckInDetail(request, pk):
    checkIns = CheckIn.objects.get(id=pk)
    serializer = CheckInSerializer(checkIns, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def CheckInCreate(request):
    serializer = CheckInSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def CheckInDelete(request, pk):
    checkIn = CheckIn.objects.get(id=pk)
    checkIn.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def CheckInUpdate(request, pk):
    checkIn = CheckIn.objects.get(id=pk)
    serializer = CheckInSerializer(instance=checkIn, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def BiomarkersList(request):
    try:
        db = firestore.client()
        biomarkers = db.collection('biomarkers')
        bio_docs = biomarkers.stream()

        bios = []
        for doc in bio_docs:
            doc_dict = doc.to_dict()
           
            for key, value in doc_dict.items():
                
                if isinstance(value, firestore.DocumentReference):
           
                    doc_dict[key] = value.id 
            bios.append(doc_dict)

        return Response(bios)
    except Exception as e:
        return Response({"error": "An error occurred while fetching biomarkers."}, status=500)


@api_view(['GET'])
@jwt_login_required
def BiomarkersDetail(request, pk):
    try:
        doc_ref = firestore.client().collection('biomarkers').document(str(pk))
        doc = doc_ref.get()
        if doc.exists:
            biomarker_data = doc.to_dict()
            return Response(biomarker_data)
        else:
            return Response({'message': 'Biomarker not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

# Ensure Firebase has been initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app()

@api_view(['POST'])
@jwt_login_required
def BiomarkersChart(request):
    try:
        user_id = request.data.get('user_id')
        time_from_str = request.data.get('time_from')
        time_to_str = request.data.get('time_to')
        biomarker = request.data.get('biomarker')  # New parameter

        if not user_id or not time_from_str or not time_to_str:
            return Response({'error': 'user_id, time_from, and time_to are required fields.'}, status=400)

        # Convert timestamp strings to datetime objects
        time_from = parse_timestamp(time_from_str)
        time_to = parse_timestamp(time_to_str)

        if not time_from or not time_to:
            return Response({'error': 'Invalid timestamp format.'}, status=400)

        # Construct the user path with prefix
        user_id_path = f"/users/{user_id}"

        # Query Firestore with the user_id_path (includes /users/ prefix)
        collection_ref = firestore.client().collection('biomarkers')
        query = collection_ref.where('user', '==', user_id_path).where('time', '>=', time_from).where('time', '<=', time_to)
        docs = query.stream()

        # Collect data from the query results
        biomarker_data = [doc.to_dict() for doc in docs]

        if biomarker_data:
            if biomarker:
                # Filter data to include only the specified biomarker and time
                filtered_data = [{'time': data.get('time'), biomarker: data.get(biomarker)} for data in biomarker_data if biomarker in data]
                return Response(filtered_data)
            else:
                return Response(biomarker_data)
        else:
            return Response({'message': 'No biomarkers found for the specified user and time range.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


def parse_timestamp(timestamp_str):
    try:
        # Parse the datetime from the timestamp string
        datetime_obj = parser.parse(timestamp_str)
        return datetime_obj
    except ValueError as e:
        print("Error parsing timestamp:", e)
        return None
    
@api_view(['POST'])
@jwt_login_required
def BiomarkersCreate(request):
    serializer = BiomarkersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def BiomarkersDelete(request, pk):
    biomarker = Biomarkers.objects.get(id=pk)
    biomarker.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def BiomarkerUpdate(request, pk):
    biomarker = Biomarkers.objects.get(id=pk)
    serializer = BiomarkersSerializer(instance=biomarker, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def GoalList(request):
    goals = Goal.objects.all()
    serializer = GoalSerializer(goals, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def GoalDetail(request, pk):
    goal = Goal.objects.get(id=pk)
    serializer = GoalSerializer(goal, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def GoalCreate(request):
    serializer = GoalSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def GoalDelete(request, pk):
    goal = Goal.objects.get(id=pk)
    goal.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def GoalUpdate(request, pk):
    goal = Goal.objects.get(id=pk)
    serializer = GoalSerializer(instance=goal, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def BadgeList(request):
    badges = Badge.objects.all()
    serializer = BadgeSerializer(badges, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def BadgeDetail(request, pk):
    badge = Badge.objects.get(id=pk)
    serializer = BadgeSerializer(badge, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def BadgeCreate(request):
    serializer = BadgeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def BadgeDelete(request, pk):
    badge = Badge.objects.get(id=pk)
    badge.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def BadgeUpdate(request, pk):
    badge = Badge.objects.get(id=pk)
    serializer = BadgeSerializer(instance=badge, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def CBTList(request):
    cbt = CBT.objects.all()
    serializer = CBTSerializer(cbt, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def CBTDetail(request, pk):
    cbt = CBT.objects.get(id=pk)
    serializer = CBTSerializer(cbt, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def CBTCreate(request):
    serializer = CBTSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def CBTDelete(request, pk):
    cbt = CBT.objects.get(id=pk)
    cbt.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def CBTUpdate(request, pk):
    cbt = CBT.objects.get(id=pk)
    serializer = CBTSerializer(instance=cbt, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def GameList(request):
    game = Game.objects.all()
    serializer = GameSerializer(game, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def GameDetail(request, pk):
    game = Game.objects.get(id=pk)
    serializer = GameSerializer(game, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def GameCreate(request):
    serializer = GameSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def GameDelete(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def GameUpdate(request, pk):
    game = Game.objects.get(id=pk)
    serializer = GameSerializer(instance=game, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def EvaluationList(request):
    evaluations = Evaluation.objects.all()
    serializer = EvaluationSerializer(evaluations, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def EvaluationDetail(request, pk):
    evaluation = Evaluation.objects.get(id=pk)
    serializer = EvaluationSerializer(evaluation, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def EvaluationCreate(request):
    serializer = EvaluationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def EvaluationDelete(request, pk):
    evaluation = Evaluation.objects.get(id=pk)
    evaluation.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def EvaluationUpdate(request, pk):
    evaluation = Evaluation.objects.get(id=pk)
    serializer = EvaluationSerializer(instance=evaluation, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def QuestionList(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def QuestionDetail(request, pk):
    question = Question.objects.get(id=pk)
    serializer = EvaluationSerializer(question, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def QuestionCreate(request):
    serializer = QuestionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def QuestionDelete(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def QuestionUpdate(request, pk):
    question = Question.objects.get(id=pk)
    serializer = QuestionSerializer(instance=question, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def HistoricalDiagnosisList(request):
    historicalDiagnosis = HistoricalDiagnosis.objects.all()
    serializer = HistoricalDiagnosisSerializer(historicalDiagnosis, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def HistoricalDiagnosisDetail(request, pk):
    historicalDiagnosis = HistoricalDiagnosis.objects.get(id=pk)
    serializer = HistoricalDiagnosisSerializer(historicalDiagnosis, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@jwt_login_required
def HistoricalDiagnosisCreate(request):
    serializer = HistoricalDiagnosisSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@jwt_login_required
def HistoricalDiagnosisDelete(request, pk):
    historicalDiagnosis = HistoricalDiagnosis.objects.get(id=pk)
    historicalDiagnosis.delete()

    return Response('Item successfully deleted!')


@api_view(['POST'])
@jwt_login_required
def HistoricalDiagnosisUpdate(request, pk):
    historicalDiagnosis = HistoricalDiagnosis.objects.get(id=pk)
    serializer = HistoricalDiagnosisSerializer(instance=historicalDiagnosis, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@jwt_login_required
def UnitList(request):
    u = Unit.objects.all()
    Unitt = UnitSerializer(u, many=True)

    return Response(Unitt.data)

@api_view(['POST'])
@jwt_login_required
def UnitCreate(request):
    serializer = UnitSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@jwt_login_required
def UnitUpdate(request, pk):
    Unittt = Unit.objects.get(id=pk)
    serializer = UnitSerializer(instance=Unittt, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@jwt_login_required
def UnitDelete(request, pk=None):
    if pk is None:
        return Response({'error': 'Primary key is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        unit = Unit.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)

    unit.delete()
    return Response({'message': 'Item successfully deleted!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_login_required
def UnitDetail(request, pk=None):
    if pk is None:
        return Response({'error': 'Primary key is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        unit = Unit.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UnitSerializer(unit, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class tags(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default=None)
    image = models.TextField()
    title = models.CharField(max_length=100, default=None)
    def __str__(self):
          return self.__all__

class majorAssessment(models.Model):
     description = models.CharField(max_length=100, default=None)
     numberOfQuestions = models.IntegerField()
     order = models.IntegerField()
     title = models.CharField(max_length=100, default=None)
 

class users(models.Model):
  #  document = models.ForeignKey(Document, on_delete=models.CASCADE)
    email = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=100, default=None)
    uid = models.CharField(max_length=100, default=None)
    display_name = models.CharField(max_length=100, default=None)

    def __str__(self):
         return self.__all__



class bites(models.Model):
  #  document = models.ForeignKey(Document, on_delete=models.CASCADE)
    # categories = models.ForeignKey(categories, on_delete=models.CASCADE)
    content = models.TextField()
    difficulty = models.IntegerField()
    tags = models.ForeignKey(tags, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    display_name=models.ForeignKey(users, on_delete=models.CASCADE)
    image= models.CharField(max_length=100)
    order=models.IntegerField()

    def __str__(self):
          return self.__all__

class collection(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    activities = models.CharField(max_length=100, default=None)
    assessmentQuestion = models.CharField(max_length=100, default=None)
    badges = models.TextField(default=None)
    biomarkers = models.TextField(default=None)
    bites = models.TextField(default=None)
    categories = models.CharField(max_length=100, default=None)
    feelings = models.CharField(max_length=100, default=None)
    inAppLinks = models.CharField(max_length=100, default=None)
    inquiry = models.CharField(max_length=100, default=None)
    items = models.CharField(max_length=100, default=None)
    journal = models.CharField(max_length=100, default=None)
    journalPrompt = models.CharField(max_length=100, default=None)
    majorAssessment = models.CharField(max_length=100, default=None)
    psychomarkers = models.CharField(max_length=100, default=None)
    scenarios = models.CharField(max_length=100, default=None)
    tags = models.ForeignKey(tags, on_delete=models.CASCADE, default=1)
    trivia = models.CharField(max_length=100, default=None)
    users = models.CharField(max_length=100, default=None)

    def __str__(self):
         return self.__all__
        
class activities(models.Model):
    #document = models.ForeignKey(Document, on_delete=models.CASCADE)
    tags = models.ForeignKey(tags, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)   
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    track= models.CharField(max_length=200)
    audiotrackId=models.CharField(max_length=100)
    audiotrackTitle=models.CharField(max_length=100)
    label=models.CharField(max_length=100)


    def __str__(self):
         return self.__all__

class assessmentQuestion(models.Model):
    majorAssessment = models.ForeignKey(majorAssessment, on_delete=models.CASCADE, default=1)
    max= models.IntegerField(default=0) 
    order= models.IntegerField(default=0)   
    points= models.IntegerField(default=0)  
    question = models.CharField(max_length=100)

class assets(models.Model):
    
    assetsType = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)

class badges(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
      return self.__all__

class biomarkers(models.Model):
    #document = models.ForeignKey(Document, on_delete=models.CASCADE)
    bloodGlucose = models.IntegerField(default=0)
    bloodGlucoseType = models.CharField(max_length=100, default=None)
    dailyActivity = models.IntegerField(default=0)
    dailyCarbs = models.IntegerField(default=0)
    weeklyActivity = models.IntegerField(default=0)
    sleepQuality = models.IntegerField(default=0)
    time = models.DateTimeField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='biomarkers_frontend')
    weight = models.IntegerField(default=0)
    FBS = models.IntegerField(default=0)
    HBA1c = models.IntegerField(default=0)

    def __str__(self):
          return self.__all__


 
class categories(models.Model):
    #document = models.ForeignKey(Document, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=100, default=None)

    def __str__(self):
       return self.__all__

class feelings(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    anger = models.BooleanField(default=False)
    fear = models.BooleanField(default=False)
    happiness = models.BooleanField(default=False)
    joy = models.BooleanField(default=False)
    love = models.BooleanField(default=False)
    sadness = models.BooleanField(default=False)
    shame = models.BooleanField(default=False)
    strength = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    time =  models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.__all__

class inAppLinks(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default=None)
    order = models.TextField()
    type = models.TextField()
    title = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.__all__

class inquiry(models.Model):
    #document = models.ForeignKey(Document, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    question = models.TextField()
    time = models.DateTimeField(default=datetime.now)
    topic = models.CharField(max_length=100, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
          return self.__all__

class items(models.Model):
    title = models.CharField(max_length=255)
    data= models.CharField(max_length=255)
    categories = models.CharField(max_length=255)



class journal(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=100, default=None)

    def __str__(self):
         return self.__all__

class journalPrompt(models.Model):
    title = models.CharField(max_length=100, default=None)

    def __str__(self):
         return self.__all__


class psychomarkers(models.Model):
    #document = models.ForeignKey(Document, on_delete=models.CASCADE)
    time =  models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    depression = models.IntegerField(default=0)

    def __str__(self):
          return self.__all__


class scenarios(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    PositiveCorrectionAlternative = models.CharField(max_length=100, default=None)
    actionreply = models.TextField()
    correction = models.TextField()
    positiveActionReply = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=100, default=None)
    
    def __str__(self):
        return self.__all__

class selfAwarenessScenarios(models.Model):
  
    correction1from0to2 = models.TextField()
    correction2from3to5 = models.TextField()
    interactiveStatement = models.TextField()
    recommendation1 = models.TextField()
    recommendation2 = models.TextField()
    scenarioID = models.CharField(max_length=100, default=None)
    story = models.TextField()
    storyTitle = models.CharField(max_length=100, default=None)
    journal= models.ForeignKey(journalPrompt, on_delete=models.CASCADE)


    def __str__(self):
        return self.__all__
    

class selfLadder(models.Model):
  
    type = models.CharField(max_length=100, default=None)
    time = models.DateTimeField()
    userID = models.ForeignKey(users, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.__all__
    

class selfAwarnessBites(models.Model):
    scenarioID = models.CharField(max_length=100, default=None)
    tags = models.CharField(max_length=100, default=None)
    selfawarenessBiteTitle = models.CharField(max_length=100, default=None)
    selfawarenessBiteText = models.TextField(max_length=100, default=None)
    def __str__(self):
        return self.selfawarenessBiteTitle
     
    
class wildCard(models.Model):
  
    content = models.TextField(max_length=100, default=None)

    def __str__(self):
        return self.__all__      

class trivia(models.Model):
  #  document = models.ForeignKey(Document, on_delete=models.CASCADE)
    CBT_points = models.IntegerField(default=0)
    answer_1 = models.CharField(max_length=100, default=None)
    answer_2 = models.CharField(max_length=100, default=None)
    answer_3 = models.TextField()
    correct_answer = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default=None)
    explanation = models.CharField(max_length=100, default=None)
    image = models.CharField(max_length=100, default=None)
    question = models.CharField(max_length=100, default=None)
    learning_points = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    topic = models.CharField(max_length=100, default=None)

    def __str__(self):
         return self.__all__



class shortBite(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default=None)
    

    def __str__(self):
         return self.__all__
    
    
    
class nutrition(models.Model):
   # document = models.ForeignKey(Document, on_delete=models.CASCADE)
    carbContent = models.CharField(max_length=100, default=None)
    name_ar = models.CharField(max_length=100, default=None)
    name_en = models.CharField(max_length=100, default=None)
    portion = models.CharField(max_length=100, default=None)
    proteinContent = models.CharField(max_length=100, default=None)
    fatContent = models.CharField(max_length=100, default=None)
    totalCalories = models.IntegerField(max_length=100, default=None)
    weight = models.CharField(max_length=100, default=None) 
    nutItem = models.CharField(max_length=100, default=None) 
    food_category = models.CharField(max_length=100, default=None) 
    Class = models.CharField(max_length=100, default=None) 
    unit = models.CharField(max_length=100, default=None) 




    
    
    def __str__(self):
         return self.__all__
from django.db import models
class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class bites(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    categories = models.CharField(max_length=100)
    content = models.TextField()
    difficulty = models.IntegerField()
    tags = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class collection(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    activities = models.CharField(max_length=100)
    badges = models.TextField()
    biomarkers = models.TextField()
    bites = models.TextField()
    categories = models.CharField(max_length=100)
    feelings = models.CharField(max_length=100)
    inquiry = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    journalPrompt = models.CharField(max_length=100)
    scenarios = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    users = models.CharField(max_length=100)

    def __str__(self):
       return self.name


class activities(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    Activity_points= models.IntegerField()
    CBT_points = models.IntegerField()
    Learning_points = models.IntegerField()
    Social_points= models.IntegerField()
    language = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    time = models.IntegerField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

     
class  badges (models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class  biomarkers (models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    Blood_glucose= models.IntegerField()
    FBS = models.IntegerField()
    HBA1c = models.IntegerField()
    height= models.IntegerField()
    sleepQuality = models.CharField(max_length=100)
    time = models.IntegerField()
    user = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)

    def __str__(self):
        return self.name













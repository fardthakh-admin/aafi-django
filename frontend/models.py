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


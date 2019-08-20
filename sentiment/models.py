from django.db import models

class Post(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    sentiment = models.FloatField()

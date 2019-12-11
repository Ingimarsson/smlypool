from django.db import models

class Shares(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  user = models.CharField()
  difficulty = models.FloatField()

from django.db import models

class Shares(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  user = models.CharField(max_length=100)
  difficulty = models.FloatField(default=0)

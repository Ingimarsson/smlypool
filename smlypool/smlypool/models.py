from django.db import models

class Shares(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  height = models.IntegerField(default=0)
  user = models.CharField(max_length=100)
  submission_diff = models.FloatField(default=0)
  actual_diff = models.FloatField(default=0)

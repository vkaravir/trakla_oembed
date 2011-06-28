from django.db import models

class Exercise(models.Model):
  code = models.CharField(max_length=255)
  height = models.SmallIntegerField()
  width = models.SmallIntegerField()
  archive = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  url = models.URLField(verify_exists=False, unique=True)

class ExerciseParameter(models.Model):
  value = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  exercise = models.ForeignKey(Exercise, related_name='parameters')
  
class ExerciseDescription(models.Model):
  exercise = models.ForeignKey(Exercise, related_name='description', unique=True)
  assignment = models.TextField()
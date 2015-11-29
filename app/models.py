"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)


class Feature(models.Model):
    description = models.CharField(max_length=255, verbose_name='Description')
    finality = models.CharField(max_length=255)
    who = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    ffile = models.FileField(upload_to='features')
    project = models.ForeignKey(Project)


class Scenario(models.Model):
    feature = models.ForeignKey(Feature, related_name='scenario')
    title = models.CharField(max_length=255)
    given = models.CharField(max_length=255)
    when = models.CharField(max_length=255)
    then = models.CharField(max_length=255)


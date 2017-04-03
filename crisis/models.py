import inspect

from django.db import models
from django.contrib.auth.models import User
import uuid
from enum import Enum


# Create your models here.

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices

class CaseType(ChoiceEnum):
    Pending = 0
    Dispatched = 1
    Resolved = 2

class CaseCategory(ChoiceEnum):
    Fire = 0
    Ambulance = 1


class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, default=1)
    longitude = models.DecimalField(max_digits=12, decimal_places=7)
    latitude = models.DecimalField(max_digits=12, decimal_places=7)
    category = models.IntegerField()
    status = models.IntegerField(choices=CaseType.choices())

class haze_PSI_24hr(models.Model):
    region = models.CharField(max_length=3)
    timestamp = models.IntegerField()
    reading = models.IntegerField()

    def __str__(self):
        return '{region} @ {timestamp} reads {reading}'.format(region=self.region,
                                                               timestamp=self.timestamp,
                                                               reading=self.reading)

    def getRegion(self):
        return self.region

    def getTimestamp(self):
        return self.timestamp

    def getReading(self):
        return self.reading

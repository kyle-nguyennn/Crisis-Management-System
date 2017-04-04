import inspect

from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
from enum import Enum


# Create your models here.

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not (m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class CaseStatus(ChoiceEnum):
    Pending = 0
    Dispatched = 1
    Resolved = 2


class UserType(ChoiceEnum):
    CallOperator = 1
    CivilDefense = 2
    Police = 3
    LTA = 4

USER_TYPE_CHOICES = [(1, 'CallOperator'), (2, 'CivilDefense'), (3, 'Police'), (4, 'LTA')]
class MyUser(AbstractUser):
    userType = models.IntegerField(choices=USER_TYPE_CHOICES, null=True)

STATUS_CHOICES = [(0, 'Pending'), (1, 'Dispatched'), (2, 'Resolved')]
class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=7)
    latitude = models.DecimalField(max_digits=12, decimal_places=7)
    category = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    detail = models.CharField(max_length=1000, default="")
    name = models.CharField(max_length=10, default="")
    phoneNum = models.CharField(max_length=10, default="")
    gender = models.CharField(max_length=10, default="")
    ic = models.CharField(max_length=8, default="")

    def __str__(self):
        return str(self.id)


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

import inspect

from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
from enum import Enum


# Create your models here.

# class ChoiceEnum(Enum):
#     @classmethod
#     def choices(cls):
#         # get all members of the class
#         members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
#         # filter down to just properties
#         props = [m for m in members if not (m[0][:2] == '__')]
#         # format into django choice tuple
#         choices = tuple([(str(p[1].value), p[0]) for p in props])
#         return choices
#
#
# class CaseStatus(ChoiceEnum):
#     Pending = 0
#     Resolving = 1
#     Closed = 2
#
#
# class UserType(ChoiceEnum):
#     CallOperator = 1
#     CivilDefense = 2
#     Police = 3
#     LTA = 4

USER_TYPE_CHOICES = [(0, 'Call Operator'), (1, 'Civil Defense'), (2, 'Police'), (3, 'Singapore power')]
class MyUser(AbstractUser):
    pass
    userType = models.IntegerField(choices=USER_TYPE_CHOICES, null=True)

STATUS_CHOICES = [(0, 'Pending'), (1, 'Resolving'), (2, 'Closed')]
CASE_CATEGORY_CHOICE = [(0,'Fire'), (1,'Traffic Accient'), (2,'Terrorist Attack'), (3, 'Gas leak')]
class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=7)
    latitude = models.DecimalField(max_digits=12, decimal_places=7)
    category = models.IntegerField(choices=CASE_CATEGORY_CHOICE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    detail = models.CharField(max_length=1000, default="")
    severity = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)
    injured = models.IntegerField(default=0)
    place_name = models.CharField(max_length=100, default="")
    region = models.IntegerField()
    name = models.CharField(max_length=20, default="")
    phoneNum = models.CharField(max_length=20, default="")
    gender = models.IntegerField(choices=[(1, 'Male'), (2,'Female')])
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

# class CaseManager(models.Model):
#     #This is a singleton
#     point = models.IntegerField()
#     crisisLevel = models.IntegerField()
#     total_number_of_case = models.IntegerField()
#     number_of_active_case = models.IntegerField()
#     number_of_resolved_case = models.IntegerField()
#     # start of making it singleton
#     class Meta:
#         abstract = True
#
#     def save(self, *args, **kwargs):
#         """
#         Save object to the database. Removes all other entries if there
#         are any.
#         """
#         self.__class__.objects.exclude(id=self.id).delete()
#         super(CaseManager, self).save(*args, **kwargs)
#
#     @classmethod
#     def load(cls):
#         """
#         Load object from the database. Failing that, create a new empty
#         (default) instance of the object and return it (without saving it
#         to the database).
#         """
#
#         try:
#             return cls.objects.get()
#         except cls.DoesNotExist:
#             return cls()
#     # end of making it singleton
#
#     def getActive(self):
#         return self.number_of_active_case
#
#     def getResolved(self):
#         return self.number_of_resolved_case
#
#     def getTotal(self):
#         return self.total_number_of_case
#
#     def getCrisisLevel(self):
#         return self.crisisLevel
#

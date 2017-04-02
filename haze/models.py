from django.db import models

# Create your models here.
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
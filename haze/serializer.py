from rest_framework import serializers
from .models import *

class PSIReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = haze_PSI_24hr
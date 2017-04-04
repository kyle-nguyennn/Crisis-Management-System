from rest_framework import serializers as rest_serializers
from .models import *
from django.core.serializers.json import Serializer
class PSIReadingSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = haze_PSI_24hr

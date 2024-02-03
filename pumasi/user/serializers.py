from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .constants import GENDER_CHOICES, BLOOD_TYPE_CHOICES

class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)
    point = serializers.IntegerField(max_value=None, min_value=None)
    introduce = serializers.CharField(max_length=200)
    child_index = serializers.IntegerField(max_value=None, min_value=None)

class ChildSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    age = serializers.IntegerField(max_value=None, min_value=None)
    blood_type = serializers.ChoiceField(choices=BLOOD_TYPE_CHOICES)
    allergies = serializers.CharField(max_length=200)
    notes = serializers.CharField(max_length=200)
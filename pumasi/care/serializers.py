from rest_framework import serializers

class CareSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=200)
    child_age = serializers.IntegerField(max_value=None, min_value=None)
    date = serializers.CharField(max_length=8)
    start_time = serializers.IntegerField(max_value=2400, min_value=0000)
    end_time = serializers.IntegerField(max_value=2400, min_value=0000)
    gender = serializers.CharField(max_length=200) # choiceField?
    status = serializers.CharField(max_length=200, default = 'waiting') # choiceField?
    email = serializers.CharField(max_length=200)

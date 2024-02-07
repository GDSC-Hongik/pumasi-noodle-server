from rest_framework import serializers
from .constants import TOPIC_CHOICES


class CommunitySerializer(serializers.Serializer):
    title           = serializers.CharField(max_length=80)
    content         = serializers.CharField(min_length=10)
    topic           = serializers.ChoiceField(choices=TOPIC_CHOICES)
    author          = serializers.EmailField()
    author_address  = serializers.CharField(read_only=True)
    like            = serializers.IntegerField(read_only=True)
    comment_count   = serializers.IntegerField(read_only=True)
    tag             = serializers.ListField(
        child=serializers.CharField(max_length=10)
    )
    created_date    = serializers.DateTimeField(read_only=True, format="%y-%m-%d %H:%M:%S")
    modify_date     = serializers.DateTimeField(read_only=True, format="%y-%m-%d %H:%M:%S")

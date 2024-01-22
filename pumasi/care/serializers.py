from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .constants import GENDER_CHOICES


class CareSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=200)
    child_age_from = serializers.IntegerField(max_value=None, min_value=None)
    child_age_to = serializers.IntegerField(max_value=None, min_value=None)
    date = serializers.CharField(max_length=8)
    start_time = serializers.IntegerField(max_value=2400, min_value=0000)
    end_time = serializers.IntegerField(max_value=2400, min_value=0000)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)  # choiceField로 바꿈
    status = serializers.CharField(max_length=200, default='waiting')
    email = serializers.CharField(max_length=200)
    id = serializers.CharField(max_length=200)

    def validate_email(self, value):
        if '@' not in value:
            raise ValidationError('유효한 이메일 주소가 아닙니다.')
        return value

    def validate(self, attrs):
        if attrs['start_time'] > attrs['end_time']:
            raise ValidationError('시간을 다시 설정하세요.')
        return attrs

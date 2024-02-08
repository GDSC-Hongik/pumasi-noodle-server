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
    rating = serializers.FloatField(max_value=5.0, min_value=0.0, default=0.0)
    # id 필드는 백엔드에서 직접 넣어주는 값이라, 데이터를 생성할 때는 없어도 되는 값.
    id = serializers.CharField(max_length=200, required=False)

    # 맡기기로 한 유저의 email과 child_id
    requester_email = serializers.CharField(max_length=200)
    requester_child_id = serializers.IntegerField(max_value=None, min_value=None)

    def validate_email(self, value):
        if '@' not in value:
            raise ValidationError('유효한 이메일 주소가 아닙니다.')
        return value

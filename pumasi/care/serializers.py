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
    rating = serializers.FloatField(max_value=5.0, min_value=0.0, default=0.0)
    # id 필드는 백엔드에서 직접 넣어주는 값이라, 데이터를 생성할 때는 없어도 되는 값.
    id = serializers.CharField(max_length=200, required=False)
    # 맡기기 요청한 유저
    requester_email = serializers.CharField(max_length=200, allow_null=True)
    requester_child_id = serializers.IntegerField(max_value=None, min_value=None)

    def validate_email(self, value):
        if '@' not in value:
            raise ValidationError('유효한 이메일 주소가 아닙니다.')
        return value

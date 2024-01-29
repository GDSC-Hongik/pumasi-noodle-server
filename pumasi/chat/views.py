from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from rest_framework import status

chat_client = FirebaseClient()


@api_view(['GET'])
def chat_list(request):
    try:
        user_email = request.user.get("email")
        if not user_email:
            raise PermissionError("유저 정보가 존재하지 않으므로 접근할 수 없습니다.")

        chat_rooms = chat_client.read_all_chat_rooms(user_email=user_email)
        return Response(chat_rooms, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({
            "error": "예상치 못한 에러가 발생하였습니다.\n" + str(ex)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def chat_detail():
    pass

@api_view(['POST'])
def chat_settings(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

def chat_message():
    pass
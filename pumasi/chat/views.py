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


@api_view(['GET'])
def chat_detail(request, room_id):
    try:
        # TODO: request 형식 유효성 검사 (아마도 시리얼라이저로)
        email = request.user.get("email")
        if not room_id:
            return Response("room_id 가 요청에 없습니다.", status=status.HTTP_400_BAD_REQUEST)

        if not chat_client.check_chat_room_exists(chat_room_id=room_id):
            return Response("존재하지 않는 채팅방입니다.", status=status.HTTP_404_NOT_FOUND)

        if not email:
            return Response("user email 정보가 없으므로 접근할 수 없습니다.", status=status.HTTP_401_UNAUTHORIZED)

        if not chat_client.check_is_user_in_chat_room(chat_room_id=room_id, user_email=email):
            return Response("user가 참여하지 않은 채팅방입니다.", status=status.HTTP_403_FORBIDDEN)

        messages = chat_client.read_all_messages(chat_room_id=room_id)
        return Response(messages, status=status.HTTP_200_OK)

    except ValueError as ex:
        return Response({
            "error": "존재하지 않는 room_id 입니다."
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({
            "error": "예상치 못한 에러가 발생하였습니다.\n" + str(ex)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def chat_settings(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

def chat_message():
    pass
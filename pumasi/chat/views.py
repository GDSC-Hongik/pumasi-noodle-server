from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from rest_framework import status

chat_client = FirebaseClient()


@api_view(['POST'])
def create_chat_room(request):
    try:
        creator = request.user.get("email")
        invite_user = request.data.get("invite_user")

        if not creator:
            return Response("로그인 user email 정보가 없으므로 접근할 수 없습니다.", status=status.HTTP_401_UNAUTHORIZED)

        if not invite_user:
            # TODO : invite_user 가 존재하는 유저인지 체크할 필요가 있을듯
            return Response("초대할 user email 정보가 없습니다.", status=status.HTTP_400_BAD_REQUEST)

        created_room_id, creator_name, invited_user_name = chat_client.create_chat_room(creator_email=creator, invite_email=invite_user)
        return Response({
            "room_id": created_room_id,
            "creator_name": creator_name,
            "invited_user_name": invited_user_name,
        }, status=status.HTTP_201_CREATED)

    except Exception as ex:
        return Response({
            "error": "예상치 못한 에러가 발생하였습니다.\n" + str(ex)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['GET', 'DELETE'])
def chat_detail(request, room_id):
    try:
        if request.method == 'GET':
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

            try:
                messages = chat_client.read_all_messages(chat_room_id=room_id)
                return Response(messages, status=status.HTTP_200_OK)

            except ValueError as ex:
                return Response({
                    "error": "존재하지 않는 room_id 입니다."
                }, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            chat_client.delete_chat_room(chat_room_id=room_id)
            return Response(status=status.HTTP_200_OK)

    except Exception as ex:
        return Response({
            "error": "예상치 못한 에러가 발생하였습니다.\n" + str(ex)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def chat_settings(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
def chat_message(request, room_id):
    try:
        # TODO: request 형식 유효성을 시리얼라이저로 체크
        message = request.data.get("message")
        email = request.user.get("email")

        if not email:
            return Response("user email 정보가 없으므로 접근할 수 없습니다.", status=status.HTTP_401_UNAUTHORIZED)

        if not message:
            return Response({
                "error": "request에 message가 없습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not chat_client.check_chat_room_exists(chat_room_id=room_id):
            return Response({
                "error": "존재하지 않는 room id 입니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not chat_client.check_is_user_in_chat_room(chat_room_id=room_id, user_email=email):
            return Response("user가 참여하지 않은 채팅방입니다.", status=status.HTTP_403_FORBIDDEN)

        chat_client.send_message(chat_room_id=room_id, user_email=email, message=message)
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as ex:
        return Response({
            "error": "예상치 못한 에러가 발생하였습니다.\n" + str(ex)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

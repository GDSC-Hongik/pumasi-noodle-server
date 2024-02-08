from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import CommunitySerializer
from .firebase_client import FirebaseClient

client = FirebaseClient()


@api_view(['GET'])
def post_list(reqeust):
    try:
        post_list_data = client.read_post_all()
        serializer = CommunitySerializer()
        return Response(
            list(map(serializer.to_representation, post_list_data)),
            status=status.HTTP_200_OK
        )
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 오류가 발생했습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def post_create(request):
    try:
        author = request.user.get("email")
        if not author:
            return Response({"error": "로그인한 유저 정보를 가져오지 못했습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        raw_data = request.data
        raw_data["author"] = author
        serializer = CommunitySerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

        post_id = client.create_post(serializer.validated_data)
        return Response({"post_id": post_id}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 오류가 발생했습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'PATCH', 'DELETE'])
def post_detail(request, post_id):
    try:
        if request.method == 'GET':
            try:
                post_data = client.read_post(post_id)
            except ValueError as ex:
                return Response({"error": str(ex)}, status=status.HTTP_404_NOT_FOUND)

            serializer = CommunitySerializer()
            return Response(serializer.to_representation(post_data), status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            author = request.user.get("email")
            if not author:
                return Response({"error": "로그인한 유저 정보를 가져오지 못했습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            if not client.check_author(post_id=post_id, check_author=author):
                return Response({"error": "작성자가 아니므로 글 수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

            data_to_put = {
                **request.data,
                "author": author
            }
            serializer = CommunitySerializer(data=data_to_put)
            serializer.is_valid(raise_exception=True)
            client.modify_post(post_id=post_id, data=serializer.validated_data)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    except ValidationError as ex:
        return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 오류가 발생했습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

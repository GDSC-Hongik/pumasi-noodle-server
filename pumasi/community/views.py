from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from .serializers import CommunitySerializer, CommentSerializer
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
                comment_serializer = CommentSerializer()
                post_data = client.read_post(post_id)
                post_data["comments"] = [
                    comment_serializer.to_representation(comment_data) for comment_data in post_data.get("comments")
                ]
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

        elif request.method == 'DELETE':
            author = request.user.get("email")
            if not author:
                return Response({"error": "로그인한 유저 정보를 가져오지 못했습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            if not client.check_author(post_id=post_id, check_author=author):
                return Response({"error": "작성자가 아니므로 글 삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

            client.delete_post(post_id=post_id)
            return Response(status=status.HTTP_200_OK)


    except ValidationError as ex:
        return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 오류가 발생했습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def post_like(request, post_id):
    try:
        client.increase_like(post_id=post_id)
        return Response(status=status.HTTP_200_OK)
    except ValueError as ex:
        return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 오류가 발생했습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def comment_create(request, post_id):
    try:
        content = request.data.get("content")
        user_email = request.user.get("email")
        if not content:
            return Response({"error": "댓글 내용이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if not user_email:
            return Response({"error": "로그인한 유저 정보가 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        client.add_comment(post_id=post_id, user_email=user_email, content=content)
        return Response(status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 오류가 발생했습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH', 'DELETE'])
def comment_modify(request: Request, post_id, comment_id):
    try:
        request_user: dict = request.user
        request_data: dict = request.data
        user = request_user.get("email")

        if not user:
            return Response({"error": "유저 정보가 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        if not client.check_comment_author(post_id=post_id, comment_id=comment_id, check_author=user):
            return Response({"error": f"{user}은 댓글 작성자가 아니므로 수정/삭제할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'PATCH':
            content_to_modify = request_data.get("content")
            if not content_to_modify:
                return Response({"error": "변경할 댓글 내용을 전달해주세요."}, status=status.HTTP_400_BAD_REQUEST)

            client.modify_comment(post_id=post_id, comment_id=comment_id, content=content_to_modify)
            return Response(status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            client.delete_comment(post_id=post_id, comment_id=comment_id)
            return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 오류가 발생했습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

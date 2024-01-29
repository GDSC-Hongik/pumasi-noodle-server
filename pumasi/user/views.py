from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from .serializers import UserSerializer, ChildSerializer

client = FirebaseClient()


@api_view(['GET'])
def UserPageView(request, pk):
    user_data = client.read_user(user_id=pk)
    # DB에서 읽어온 user_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
    serializer = UserSerializer(user_data)
    return Response(serializer.data)


@api_view(['GET'])
def ChildList(request, pk):
    child_data = client.read_child_all(user_id=pk)
    # DB에서 읽어온 child_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
    serializer = ChildSerializer(child_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ChildDetail(request, pk, child_pk):
    child_doc_data = client.read_child(user_id=pk, child_number=child_pk)
    serializer = ChildSerializer(child_doc_data, many=True)
    return Response(serializer.data)
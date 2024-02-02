from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from .serializers import UserSerializer, ChildSerializer
from .add_data import add_user_data_to_firestore, add_child_data_to_firestore

client = FirebaseClient()

@api_view(['GET'])
def UserList(request):
    user_list_data = client.read_user_all()
    # DB에서 읽어온 user_list_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
    serializer = UserSerializer(user_list_data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH'])
def UserDetail(request, pk):
    if request.method == 'GET':
        user_data = client.read_user(user_id=pk)
        # DB에서 읽어온 user_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
        serializer = UserSerializer(user_data)
        return Response(serializer.data)

    if request.method == 'PATCH':
        user_data = client.read_user(user_id=pk)
        serializer = UserSerializer(user_data, many=True)
        # DB에서 읽어온 user_data 값을 시리얼라이저를 통한 유효성 검사
        if not serializer.is_valid():
            print("validation error")
            return Response({
                "error": "request body로 들어온 값이 유효하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST)

        client.update_user(user_id=pk, update_data=request.data)


@api_view(['GET'])
def ChildList(request, pk):
    child_data = client.read_child_all(user_id=pk)
    # DB에서 읽어온 child_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
    serializer = ChildSerializer(child_data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH'])
def ChildDetail(request, pk, child_pk):
    if request.method == 'GET':
        child_doc_data = client.read_child(user_id=pk, child_number=child_pk)
        # DB에서 읽어온 child_doc_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
        serializer = ChildSerializer(child_doc_data, many=True)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        child_doc_data = client.read_child(user_id=pk, child_number=child_pk)
        serializer = ChildSerializer(child_doc_data, many=True)
        # DB에서 읽어온 child_doc_data 값을 시리얼라이저를 통한 유효성 검사
        if not serializer.is_valid():
            print("validation error")
            return Response({
                "error": "request body로 들어온 값이 유효하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST)

        client.update_child(user_id=pk, child_number=child_pk, update_data=request.data)


@api_view(['DELETE'])
def ChildDelete(request, pk, child_pk):
    client.delete_child(user_id=pk, child_number=child_pk)


@api_view(['GET'])
def AddUserData(request):
    add_user_data_to_firestore()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def AddChildData(request):
    add_child_data_to_firestore()
    return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from .serializers import UserSerializer, ChildSerializer, CareSerializer
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


@api_view(['GET', 'POST'])
def ChildList(request, pk):
    if request.method == 'GET':
        child_data = client.read_child_all(user_id=pk)
        # DB에서 읽어온 child_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
        serializer = ChildSerializer(child_data, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        new_data = request.data
        serializer = ChildSerializer(data=new_data)
        if serializer.is_valid():
            client.create_child(user_id=pk, child_data=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
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

    if request.method == 'DELETE':
        client.delete_child(user_id=pk, child_number=child_pk)


# 실제 사용하는 기능 아님
@api_view(['GET'])
def AddUserData(request):
    add_user_data_to_firestore()
    return Response(status=status.HTTP_204_NO_CONTENT)


# 실제 사용하는 기능 아님
@api_view(['POST'])
def AddUserDataPost(request, pk):
    new_data = request.data
    serializer = UserSerializer(new_data, many=True)
    if serializer.is_valid():
        client.create_user(user_id=pk, user_data=serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 실제 사용하는 기능 아님
@api_view(['GET'])
def AddChildData(request):
    add_child_data_to_firestore()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def UserCareList(request, pk):
    care_list_data = client.read_user_care_all(user_id=pk)
    # DB에서 읽어온 care_list_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
    serializer = CareSerializer(care_list_data)
    return Response(serializer.data)


@api_view(['GET'])
def UserCareDetail(request, pk, child_pk):
    care_detail_data = client.read_user_care_detail(user_id=pk, child_id=child_pk)
    # DB에서 읽어온 care_detail_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
    serializer = CareSerializer(care_detail_data, many=True)
    return Response(serializer.data)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firebase_client import FirebaseClient
from .serializers import CareSerializer

client = FirebaseClient()

# Create your views here.
@api_view(['GET'])
def care_list(request):
    care_list_data = client.read_care_all()
    # DB에서 읽어온 care_list_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환
    serializer = CareSerializer(care_list_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def care_detail(request, pk):
    if request.method == 'GET':
        print("get a care data")
        try:
            care_data = client.read_care(user_email=pk)
            # DB에서 읽어온 care_data 값을 시리얼라이저를 활용하여 Response 형식으로 변환 
            serializer = CareSerializer(care_data, many=True)
        except ValueError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


@api_view(['POST', 'PATCH'])
def my_care(request):
    if request.method == 'POST':
        print("create my care data")
        # my_email = request.user.email
        my_email = "test3@example.com" # 로그인 구현이 안되어 있으므로, 테스트 이메일 사용

        # request.data 값을 시리얼라이저를 활용하여 유효성 검사 
        serializer = CareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client.create_care(user_email=my_email, care_data=request.data)

        return Response(request.data, status=status.HTTP_201_CREATED)

    if request.method == 'PATCH':
        print("modify my care data")
        # my_email = request.user.email
        my_email = "test3@example.com" # 로그인 구현이 안되어 있으므로, 테스트 이메일 사용
        
        # request.data 값을 시리얼라이저를 활용하여 유효성 검사 
        serializer = CareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        client.update_care(user_email=my_email, update_data=request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['PUT'])
def update_status(request, pk):
    stat = request.data.get("status")
    if not stat:
        return Response({"error": str("status가 전달되지 않았습니다.")}, status=status.HTTP_400_BAD_REQUEST)

    if stat in ["waiting", "reserved", "accepted"]:
        client.update_care_status(user_email=pk, status=stat)
    else:
        return Response(
            {"error": str("잘못된 status 값 입니다. waiting, reserved, accepted 중에서 골라야합니다.")},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(status=status.HTTP_204_NO_CONTENT)
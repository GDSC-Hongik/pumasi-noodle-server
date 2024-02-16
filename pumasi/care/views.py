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


@api_view(['POST', 'PATCH', 'DELETE'])
def my_care(request):
    my_email = request.user.get("email")
    print(my_email)

    if request.method == 'POST':
        # request.data 값을 시리얼라이저를 활용하여 유효성 검사 
        serializer = CareSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            print("validation error")
            return Response({
                "error": "request body로 들어온 값이 유효하지 않습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        print(serializer.data)
        client.create_care(user_email=my_email, care_data=serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'PATCH':
        # request 데어터 형식이 시리얼라이저와 맞지 않으므로 주석처리
        # serializer = CareSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        
        client.update_care(user_email=my_email, update_data=request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'DELETE':
        client.delete_care(user_email=my_email)
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


@api_view(['POST'])
def request_care(request, pk):
    try:
        requester_email = request.user.get("email")
        child_id = request.data.get("child_id")
        if not requester_email:
            return Response({"error": "로그인 유저의 정보가 누락되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        if not child_id:
            return Response({"error": "child_id 가 요청 데이터에 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        client.request_care(care_id=pk, requester_email=requester_email, requester_child_id=child_id)
        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 에러가 발생하였습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def complete_care(request, pk):
    try:
        requester_email = request.user.get("email")
        point = request.data.get("point")
        rating = request.data.get("rating")

        if not requester_email:
            return Response({"error": "로그인 유저의 정보가 누락되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        if not point or not rating:
            return Response({"error": "point, rating 정보가 모두 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not client.check_requester(care_id=pk, requester_email=requester_email):
            return Response({"error": "맡기기를 요청한 유저가 아니므로, 맡기를 완료할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        client.complete_care(care_id=pk, care_rating=rating, point=point)
        return Response(status=status.HTTP_200_OK)
    except ValueError as ex:
        return Response({"error": f"잘못된 요청입니다.\n{str(ex)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(
            {"error": "의도치 않은 에러가 발생하였습니다.\n" + str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
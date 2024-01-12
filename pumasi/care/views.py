from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from firebase_admin import firestore
DB = firestore.client()

# Create your views here.
@api_view(['GET'])
def care_list(request):
    """
    하나의 컬렉션에서 여러개의 문서를 읽어오는 방법 (컬렉션에서 여러 문서 가져오기 파트)
    => https://firebase.google.com/docs/firestore/query-data/get-data?hl=ko
    """
    care_list = []
    for care in DB.collection("care").stream():
        id = care.id
        care = care.to_dict()
        care["id"] = id
        care_list.append(care)
    return Response(care_list, status=status.HTTP_200_OK)


@api_view(['GET'])
def care_detail(request, pk):
    if request.method == 'GET':
        print("get a care data")
        try:
            care_data = DB.collection("care").document(pk).get().to_dict()
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(care_data, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
def my_care(request):
    if request.method == 'POST':
        print("create my care data")
        DB.collection("care").add(request.data)
        return Response(request.data, status=status.HTTP_201_CREATED)

    if request.method == 'PATCH':
        print("get a care data")
        return Response({"method": "patch", "from": "care"}, status=200)
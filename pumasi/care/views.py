from rest_framework.decorators import api_view
from rest_framework.response import Response
from firebase_admin import firestore

# Create your views here.
@api_view(['GET'])
def care_list(request):
    print("care list")
    return Response({}, status=200)


@api_view(['GET'])
def care_detail(request, pk):
    if request.method == 'GET':
        print("get a care data")
        return Response({"method": "get", "from": "care", "pk": pk}, status=200)


@api_view(['POST', 'PATCH'])
def my_care(request):
    if request.method == 'POST':
        print("get a care data")
        return Response({"method": "post", "from": "care"}, status=200)

    if request.method == 'PATCH':
        print("get a care data")
        return Response({"method": "patch", "from": "care"}, status=200)
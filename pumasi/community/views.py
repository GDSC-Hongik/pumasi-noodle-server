from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def post_list(reqeust):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
def post_create(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'PATCH', 'DELETE'])
def post_detail(reqeust, post_id):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

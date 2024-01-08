from rest_framework.decorators import api_view
from rest_framework.response import Response
from firebase_admin import firestore

@api_view(['GET'])
def index(request):
    db = firestore.client()
    return Response(db.collection("test").document("test").get().to_dict(), status=200)
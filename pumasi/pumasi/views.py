import json

from requests.exceptions import HTTPError
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from firebase_admin import auth, firestore

from .settings import pyrebase_app

@api_view(['GET'])
@authentication_classes([])
def index(request):
    """
    settings.py 에서 데이터베이스 접속 정보를 .env 파일로부터 가져온 뒤, 그 정보를 토대로 데이터베이스와 연결까지 해둠.
    (-> 최초 1회만 실행해야 하기 때문에 settings.py 에서 코드를 작성함)

    collection(컬렉션) 이 무엇인가 / document(문서) 가 무엇인가
    -> https://firebase.google.com/docs/firestore/data-model?hl=ko
    """

    # db 변수에 settings.py에서 연결한 데이터베이스 객체를 저장. 이 객체를 통해서 데이터베이스를 읽고 쓸 수 있음.
    # 앞으로 DB를 다룰 때마다 이 코드를 통해 데이터베이스 객체를 가져오면 됨.
    db = firestore.client()

    # DB 에서 "test" 라는 이름의 컬렉션 객체를 가져옴.
    test_collection = db.collection("test")

    # "test" 컬렉션에서 "test" 라는 이름의 문서를 가져옴. (정확히는 해당 문서의 reference 객체를 가져옴)
    test_document_ref = test_collection.document("test")

    # reference 객체는 말 그대로 그 문서를 가리키고 있을 뿐이라 실제 문서 데이터는 갖고 있지 않음.
    # reference로 부터 실제 데이터를 가져올 때는 .get() 메서드를 이용함.
    test_data = test_document_ref.get()

    # 가져온 데이터를 딕셔너리로 바꿔줌. Response는 딕셔너리를 받아서 JSON 으로 변환하기 때문.
    data = test_data.to_dict()

    # 지금까지 분리해서 코드를 작성했지만 이런 식으로 이어서 작성할 수 있음.
    # data = db.collection("test").document("test").get().to_dict()
    """
        Firestore 데이터 읽기
        -> https://firebase.google.com/docs/firestore/query-data/get-data?hl=ko
        
    """
    return Response(data, status=200)

@api_view(['POST'])
@authentication_classes([])
def login(request):
    try:
        pyrebase_auth = pyrebase_app.auth()
        user = pyrebase_auth.sign_in_with_email_and_password(
            **request.data
            # email=request.data["email"],
            # password=request.data["password"]
        )
        return Response(user)
    except HTTPError as ex:
        error_data = json.loads(str(ex))
        print(error_data)
        return Response(
            {"error": str(ex)},
            status=status.HTTP_400_BAD_REQUEST
        )

    except ParseError as ex:
        return Response(
            {"error": "JSON 형식이 잘못되어 파싱할 수 없습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as ex:
        print(ex)
        print(ex.__class__)
        print(ex.args)
        return Response(
            {"error": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def logout(request):
    try:
        print(request.user)
        auth.revoke_refresh_tokens(request.user.get('uid'))
        # 놀랍게도 로그아웃 메서드가 없다...
        return Response()
    except Exception as ex:
        return Response(
            {"error": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([])
def register(request):
    try:
        user = auth.create_user(
            **request.data
            # email=request.data["email"],
            # password=request.data["password"]
        )
        return Response(user.email)
    except Exception as ex:
        return Response(
            {"error": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
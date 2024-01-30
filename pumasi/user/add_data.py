from firebase_admin import firestore
from .firebase_client import FirebaseClient

# Firestore 데이터 추가 예제
def add_data_to_firestore():
    client = FirebaseClient()
    # Firestore 데이터
    data_to_add = {
        'name': 'John Doe',
        'address': '서울특별시 마포구 서교동 357-1',
        'point': 70,
        'introduce': '내 아이처럼 소중하게 보살피겠습니다'
    }

    # Firestore 데이터베이스 컬렉션 참조
    users_ref = client.collection('users')

    # 데이터 추가
    doc_ref = users_ref.add(data_to_add)

    print('Document written with ID:', doc_ref.id)

# 함수 호출
add_data_to_firestore()
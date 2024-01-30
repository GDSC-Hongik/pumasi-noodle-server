from firebase_admin import firestore
from .firebase_client import FirebaseClient

def add_data_to_firestore():
    client = FirebaseClient()
    # Firestore 데이터
    data_to_add = {
        'name': 'John Doe',
        'address': '서울특별시 마포구 서교동 357-1',
        'point': 70,
        'introduce': '내 아이처럼 소중하게 보살피겠습니다'
    }

    client.collection("users").document("test@example.com").set(data_to_add)



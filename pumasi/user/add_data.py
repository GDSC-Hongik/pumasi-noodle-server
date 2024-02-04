from firebase_admin import firestore
from .firebase_client import FirebaseClient

def add_user_data_to_firestore():
    client = FirebaseClient()

    # 추가할 유저 데이터
    user_data_to_add = {
        'name': 'John Doe',
        'address': '서울특별시 마포구 서교동 357-1',
        'point': 70,
        'introduce': '내 아이처럼 소중하게 보살피겠습니다',
        'child_index': 1
    }

    client.create_user("test@example.com", user_data_to_add)


def add_child_data_to_firestore():
    client = FirebaseClient()

    # 추가할 아이 데이터
    child_data_to_add_1 = {
        'name': '아이1',
        'gender': 'm',
        'age': 6,
        'blood_type': 'AB',
        'allergies': '없음',
        'notes': '낯을 가림'
    }
    child_data_to_add_2 = {
        'name': '아이2',
        'gender': 'f',
        'age': 11,
        'blood_type': 'A',
        'allergies': '복숭아 알러지',
        'notes': '애착인형이 있어야 잠을 잠'
    }

    client.create_child("test@example.com", child_data_to_add_1)
    client.create_child("test@example.com", child_data_to_add_2)
import firebase_admin
from firebase_admin import firestore

class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._user_collection = self._db.collection("user")

    # user 문서의 정보를 가져온다
    def read_user(self, user_id):
        print(user_id)
        user_page_doc = self._user_collection.document(user_id).get()
        if user_page_doc.exists:
            my_page = user_page_doc.to_dict()
        else:
            raise ValueError(f"user {user_id} doesn't exist.")
        return my_page

    # user 문서의 하위 컬렉션 child에서 모든 문서를 가져온다
    def read_child_all(self, user_id):
        print(user_id)

        child_collection = self._db.collection("user").document(user_id).collection("Child")
        docs = child_collection.stream()

        for doc in docs:
            return [{**doc.to_dict(), "id": doc.id}]
        
    # user 문서의 하위 컬렉션 child에서 개별 문서를 가져온다
    def read_child(self, user_id, child_number):
        print(user_id)
        print(child_number)

        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_doc = child_collection.document(child_number).get()
        if child_doc.exists:
            child_page = child_doc.to_dict()
        else:
            raise ValueError(f"child {child_number} doesn't exist.")
        return child_page
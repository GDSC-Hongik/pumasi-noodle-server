import firebase_admin
from firebase_admin import firestore

class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._user_collection = self._db.collection("user")


    ### user 문서
    
    # 모든 user 문서의 정보를 가져온다
    def read_user_all(self):
        docs = self._user_collection.stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]

    # 개별 user 문서의 정보를 가져온다
    def read_user(self, user_id):
        print(user_id)
        user_page_doc = self._user_collection.document(user_id).get()
        if user_page_doc.exists:
            my_page = user_page_doc.to_dict()
        else:
            raise ValueError(f"user {user_id} doesn't exist.")
        return my_page

    # user 문서를 생성한다
    def create_user(self, user_id, user_data):
        self._user_collection.document(user_id).set(user_data)

    # user 문서의 정보를 수정한다
    def update_user(self, user_id, update_data):
        self._user_collection.document(user_id).update(update_data)


    ### child 문서
    
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

    # child 문서를 생성한다
    def create_child(self, user_id, child_number, child_data):
        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_collection.document(child_number).set(child_data)

    # child 문서의 정보를 수정한다
    def update_child(self, user_id, child_number, update_data):
        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_collection.document(child_number).update(update_data)

    # child 문서를 삭제한다
    def delete_child(self, user_id, child_number):
        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_doc_to_delete = child_collection.document(child_number)
        child_doc_to_delete.delete()
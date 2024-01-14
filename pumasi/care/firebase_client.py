import firebase_admin
from firebase_admin import firestore


class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._care_collection = self._db.collection("care")

    def create_care(self, user_email, care_data):
        self._care_collection.document(user_email).set(care_data)

    def update_care(self, user_email, update_data):
        self._care_collection.document(user_email).update(update_data)

    def read_care_all(self):
        """
        하나의 컬렉션에서 여러개의 문서를 읽어오는 방법 (컬렉션에서 여러 문서 가져오기 파트)
        => https://firebase.google.com/docs/firestore/query-data/get-data?hl=ko
        """
        docs = self._care_collection.stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]

    def read_care(self, user_email):
        print(user_email)
        care_doc = self._care_collection.document(user_email).get()
        if care_doc.exists:
            care = care_doc.to_dict()
        else:
            raise ValueError(f"care document for {user_email} doesn't exist.")
        return care
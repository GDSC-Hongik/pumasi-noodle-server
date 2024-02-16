import firebase_admin
from firebase_admin import firestore
from firebase_admin.firestore import firestore as fs
from google.cloud.firestore_v1 import DocumentReference, CollectionReference, DocumentSnapshot
from .constants import CARE_ACCEPTED


class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._care_collection: CollectionReference = self._db.collection("care")
        self._user_collection: CollectionReference = self._db.collection("user")

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

    def update_care_status(self, user_email, status):
        care_ref = self._care_collection.document(user_email)
        if care_ref.get().exists:
            care_ref.update({
                "status": status
            })
        else:
            raise ValueError(f"care document for {user_email} doesn't exist.")

    def delete_care(self, user_email):
        try:
            self._care_collection.document(user_email).delete()
        except Exception as ex:
            print("firebase_client.py delete_care, error was occured while deleting care data")
            raise ex

    def request_care(self, care_id, requester_email, requester_child_id):
        try:
            care_ref = self._care_collection.document(care_id)
            if care_ref.get().exists:
                care_ref.update({
                    "requester_email": requester_email,
                    "requester_child_id": requester_child_id,
                    "status": "reserved"
                })
            else:
                raise ValueError(f"care document for {care_id} doesn't exist.")
        except Exception as ex:
            raise ex

    def complete_care(self, care_id: str, care_rating: float, point: int):
        care_ref: DocumentReference = self._care_collection.document(care_id)
        care_snapshot: DocumentSnapshot = care_ref.get()

        if not care_snapshot.exists:
            raise ValueError(f"care document for {care_id} doesn't exist.")

        requester_email: str    = care_snapshot.get("requester_email")
        care_status: str        = care_snapshot.get("status")
        rating_count: int       = care_snapshot.get("rating_count")
        rating: float           = care_snapshot.get("rating")

        if care_status != "reserved":
            raise ValueError(f"care document's status for {care_id} should be 'reserved'")

        carer_email = care_id
        requester_ref: DocumentReference = self._user_collection.document(requester_email)
        carer_ref: DocumentReference = self._user_collection.document(carer_email)

        if not requester_ref.get().exists:
            raise ValueError(f"user document for {requester_email} doesn't exist.")

        requester_point = requester_ref.get().get("point")
        if requester_point < point:
            raise ValueError(f"care requester {requester_email}'s point is not enough")

        if not carer_ref.get().exists:
            raise ValueError(f"user document for {carer_email} doesn't exist.")

        new_rating = round((rating_count * rating + care_rating) / (rating_count + 1), ndigits=1)

        care_ref.update({
            "status": CARE_ACCEPTED,
            "rating_count": fs.Increment(1),
            "rating": new_rating,
        })

        requester_ref.update({
            "point": fs.Increment(-point)
        })

        carer_ref.update({
            "point": fs.Increment(point)
        })

    def check_requester(self, care_id: str, requester_email: str):
        care_snapshot = self._care_collection.document(care_id).get()
        if not care_snapshot.exists:
            raise ValueError(f"care document for {care_id} doesn't exist.")

        return care_snapshot.get("requester_email") == requester_email

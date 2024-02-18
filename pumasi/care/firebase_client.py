import firebase_admin
from firebase_admin import firestore
from firebase_admin.firestore import firestore as fs
from google.cloud.firestore_v1 import DocumentReference, CollectionReference, DocumentSnapshot
from .constants import CARE_ACCEPTED, CARE_WAITING


class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._care_collection: CollectionReference = self._db.collection("care")
        self._user_collection: CollectionReference = self._db.collection("user")

    def create_care(self, user_email, care_data):
        user_doc: DocumentSnapshot = self._user_collection.document(user_email).get()

        if not user_doc.exists:
            raise ValueError(f"user document for {user_email} doesn't exist.")

        user_name = user_doc.get("name")
        self._care_collection.document(user_email).set({
            **care_data,
            "rating": 0.0,
            "rating_count": 0,
            "user_name": user_name
        })

    def update_care(self, user_email, update_data):
        self._care_collection.document(user_email).update(update_data)

    def read_care_all(self):
        docs = self._care_collection.where(filter=fs.FieldFilter("status", "==", CARE_WAITING)).stream()
        result = []
        for doc in docs:
            name = self._user_collection.document(doc.id).get().get("name")
            result.append({
                **doc.to_dict(),
                "id": doc.id,
                "user_name": name
            })
        return result

    def read_care(self, user_email):
        care_doc: DocumentSnapshot = self._care_collection.document(user_email).get()
        user_doc: DocumentSnapshot = self._user_collection.document(user_email).get()

        if not care_doc.exists:
            raise ValueError(f"care document for {user_email} doesn't exist.")

        if not user_doc.exists:
            raise ValueError(f"user document for {user_email} doesn't exist.")

        care_data = care_doc.to_dict()
        if "user_name" not in care_data.keys():
            care_data["user_name"] = user_doc.get("name")

        print(care_data)
        return care_data

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
            if not care_ref.get().exists:
                raise ValueError(f"care document for {care_id} doesn't exist.")

            if care_ref.get().get("status") != CARE_WAITING:
                raise ValueError(f"care document for {care_id}'s status should be {CARE_WAITING}")

            care_ref.update({
                "requester_email": requester_email,
                "requester_child_id": requester_child_id,
                "status": "reserved"
            })
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

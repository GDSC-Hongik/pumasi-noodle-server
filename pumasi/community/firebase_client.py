from firebase_admin import firestore
from firebase_admin.firestore import firestore as fs
import datetime


class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._community_collection = self._db.collection("community")
        self._user_collection = self._db.collection("user")

    def read_post_all(self):
        docs = self._community_collection.stream()
        return [doc.to_dict() for doc in docs]

    def read_post(self, post_id):
        post_snapshot = self._community_collection.document(post_id).get()
        if not post_snapshot.exists:
            raise ValueError(f"no post with id {post_id}")

        return post_snapshot.to_dict()

    def create_post(self, post_data):
        author = post_data.get("author")
        if not author:
            raise AttributeError("no 'author' data in post_data")

        author_snapshot = self._user_collection.document(author).get()
        if not author_snapshot.exists:
            raise AttributeError(f"no user {author}'s document in user collection")

        address = author_snapshot.get("address")
        if not address:
            print(address)
            raise AttributeError(f"no 'address' data in user {author}'s document")

        created_time, doc_ref = self._community_collection.add({
            **post_data,
            "author_address": address,
            "like": 0,
            "comment_count": 0,
            "created_date": fs.SERVER_TIMESTAMP,
            "modify_date": fs.SERVER_TIMESTAMP,
        })

        return doc_ref.get().id

    def modify_post(self, post_id, data):
        post_doc = self._community_collection.document(post_id)
        post_doc.update({
            **data,
            "modify_date": fs.SERVER_TIMESTAMP,
        })

    def check_author(self, post_id, check_author):
        author = self._community_collection.document(post_id).get().get("author")
        return author == check_author

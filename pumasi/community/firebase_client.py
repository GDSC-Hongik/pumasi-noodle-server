from firebase_admin import firestore
from google.cloud.firestore_v1 import Client, CollectionReference
from firebase_admin.firestore import firestore as fs
import datetime


class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db : Client = firestore.client()
        self._community_collection = self._db.collection("community")
        self._user_collection = self._db.collection("user")

    def read_post_all(self):
        docs = self._community_collection.stream()
        return [{
            **doc.to_dict(),
            "post_id": doc.id,
            "comment_count": doc.reference.collection("comments").count().get()[0][0].value
        } for doc in docs]

    def read_post(self, post_id):
        post_ref = self._community_collection.document(post_id)
        post_snapshot = post_ref.get()
        if not post_snapshot.exists:
            raise ValueError(f"no post with id {post_id}")

        post_data = post_snapshot.to_dict()

        comments_ref = post_ref.collection("comments").order_by("created_date", direction=fs.Query.ASCENDING).stream()
        comments_data = [{ **comment.to_dict(), "comment_id": comment.id } for comment in comments_ref]
        post_data["comment_count"] = len(comments_data)
        return {
            **post_data,
            "comments": comments_data
        }

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

    def increase_like(self, post_id):
        post_doc = self._community_collection.document(post_id)
        if not post_doc.get().exists:
            raise ValueError(f"Post ID {post_id} doesn't exist")
        post_doc.update({
            "like": fs.Increment(1)
        })

    def delete_post(self, post_id):
        post_doc = self._community_collection.document(post_id)
        post_doc.delete()

    def add_comment(self, post_id, user_email, content):
        user_snapshot = self._user_collection.document(user_email).get()
        if not user_snapshot.exists:
            raise AttributeError(f"no user {user_email}'s document in user collection")

        name = user_snapshot.get("name")
        if not name:
            raise AttributeError(f"no 'name' data in user {user_snapshot}'s document")

        self._community_collection.document(post_id).collection("comments").add({
            "content": content,
            "user_email": user_email,
            "user_name": name,
            "created_date": fs.SERVER_TIMESTAMP,
        })

    def modify_comment(self, post_id, comment_id, content):
        comments_collection: CollectionReference = self._community_collection.document(post_id).collection("comments")
        comments_collection.document(comment_id).update({"content": content})

    def delete_comment(self, post_id, comment_id):
        comments_collection: CollectionReference = self._community_collection.document(post_id).collection("comments")
        comments_collection.document(comment_id).delete()

    def check_author(self, post_id, check_author):
        author = self._community_collection.document(post_id).get().get("author")
        return author == check_author

    def check_comment_author(self, post_id, comment_id, check_author):
        comments_collection: CollectionReference = self._community_collection.document(post_id).collection("comments")
        author = comments_collection.document(comment_id).get().get("user_email")
        return check_author == author

from firebase_admin import firestore
from firebase_admin.firestore import firestore as fs
import datetime


class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._chat_collection = self._db.collection("chat")

    def create_chat_room(self, chat_room_data):
        self._chat_collection.add({
            "messages": [],
            "members": []
        })

    def send_message(self, chat_room_id, user_email, message):
        chat_doc = self._chat_collection.document(chat_room_id).get()
        if not chat_doc.exists:
            raise ValueError(f"chat document for {chat_room_id} doesn't exist.")

        self._chat_collection.document(chat_room_id).update({
            "messages": fs.ArrayUnion([{
                "sender": user_email,
                "message": message,
                "send_time": datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
            }])
        })

    def read_all_messages(self, chat_room_id):
        chat_doc = self._chat_collection.document(chat_room_id).get()
        if chat_doc.exists:
            messages = chat_doc.to_dict().get("messages")
            return messages

        raise ValueError(f"chat document for {chat_room_id} doesn't exist.")

    def update_chat_room_settings(self, chat_room_id, settings):
        chat_doc = self._chat_collection.document(chat_room_id).get()
        if chat_doc.exists:
            chat_doc.update({
                "settings": settings
            })
        else:
            raise ValueError(f"chat document for {chat_room_id} doesn't exist.")
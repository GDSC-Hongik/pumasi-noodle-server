import firebase_admin
from firebase_admin import firestore

class FirebaseClient:
    def __init__(self) -> None:
        # firebase app is set in 'settings.py'
        self._db = firestore.client()
        self._user_collection = self._db.collection("user")
        self._care_collection = self._db.collection("care")


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

        result = []
        for doc in docs:
            result.append({**doc.to_dict(), "child_id": doc.id})

        return result

    # user 문서의 하위 컬렉션 child에서 개별 문서를 가져온다
    def read_child(self, user_id, child_number):
        print(user_id)
        print(child_number)

        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_doc = child_collection.document(str(child_number)).get()
        if child_doc.exists:
            child_page = child_doc.to_dict()
        else:
            raise ValueError(f"child {child_number} doesn't exist.")
        return child_page

    # child 문서를 생성한다
    def create_child(self, user_id, child_data):

        ### child 문서의 id을 지정하기 위한 index를 user 문서에서 가져온다
        user_doc_ref = self._user_collection.document(user_id)
        user_doc_snapshot = user_doc_ref.get()

        if user_doc_snapshot.exists:
            index = user_doc_snapshot.to_dict()['child_index']
            print('child_index:', index)
        else:
            raise ValueError(f"user {user_id} doesn't exist.")

        ### 받아온 index를 id로 가지는 child 문서를 생성한다.
        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_collection.document(str(index)).set(child_data)

        ### user 문서의 index를 update해준다.
        index = index + 1
        update_index = {'child_index': index}

        # 문서 업데이트
        user_doc_ref.update(update_index)

    # child 문서의 정보를 수정한다
    def update_child(self, user_id, child_number, update_data):
        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_collection.document(str(child_number)).update(update_data)

    # child 문서를 삭제한다
    def delete_child(self, user_id, child_number):
        child_collection = self._db.collection("user").document(user_id).collection("Child")
        child_doc_to_delete = child_collection.document(str(child_number))
        child_doc_to_delete.delete()

    
    ### care 데이터
    
    # 현재 유저(가 맡기기로 한) care 데이터 문서들을 모두 가져온다
    def read_user_care_all(self, user_id):
        docs = self._care_collection.stream()
        result = []
        
        for doc in docs:
            doc_snapshot = doc.get(None)
            requester_email = doc_snapshot.get("requester_email")
            requester_child_id = doc_snapshot.get("requester_child_id")
            status = doc_snapshot.get("status")

            if requester_email and requester_child_id:

                # 가져온 care 문서들 중 requester_email 필드가 user_id와 같고 status가 accepted인 것들을 모아 반환
                if requester_email == user_id and status == 'reserved':
                    result.append({**doc.to_dict(), "id": doc.id})
            
            else:
                pass
            
        return result

    # 현재 유저(가 맡기기로 한) care 데이터 문서들 중 특정 문서를 가져온다
    def read_user_care_detail(self, user_id, child_id):
        docs = self._care_collection.stream()
        result = []
        
        for doc in docs:
            doc_snapshot = doc.get(None)
            requester_email = doc_snapshot.get("requester_email")
            requester_child_id = doc_snapshot.get("requester_child_id")

            if requester_email and requester_child_id:

                # 가져온 care 문서들 중 requester_email, requester_child_id 필드가 각각 user_id, child_id 와 일치하는 문서를 찾아 반환한다
                if requester_email == user_id and requester_child_id == child_id:
                    result.append({**doc.to_dict(), "id": doc.id})
                    break
            
            else:
                pass

        return result
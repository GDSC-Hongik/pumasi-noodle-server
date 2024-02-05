from django.test import TestCase
from .firebase_client import FirebaseClient
# Create your tests here.
class CareFirebaseClientTest(TestCase):
    def setUp(self) -> None:
        self.firebase_client = FirebaseClient()
        self.user_email = "test@example.com"

    def test_맡기_데이터에_대한_맡기기_요청_테스트(self):
        self.firebase_client.create_care(user_email="맡기_데이터에_대한_맡기기_요청_테스트", care_data={})
        self.firebase_client.request_care(
            care_id="맡기_데이터에_대한_맡기기_요청_테스트",
            requester_email=self.user_email,
            requester_child_id=1
        )
        care_doc_data = self.firebase_client.read_care(user_email="맡기_데이터에_대한_맡기기_요청_테스트")
        self.assertTrue(
            care_doc_data.get("requester_email") is not None
            and care_doc_data.get("requester_child_id") is not None
            and care_doc_data.get("status") == "reserved"
        )
        self.firebase_client.delete_care(user_email="맡기_데이터에_대한_맡기기_요청_테스트")
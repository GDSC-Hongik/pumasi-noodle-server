from rest_framework import authentication, exceptions
from firebase_admin import auth

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print(request.META)
        id_token = request.META.get('HTTP_AUTHORIZATION')
        if not id_token:
            raise Exception("No ID Token")

        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        except:
            raise Exception("Invalid ID Token")

        user = {
            "uid": decoded_token.get('uid'),
            "email": decoded_token.get('firebase').get('identities').get('email')[0]
        }

        print(user)

        return (user, None)
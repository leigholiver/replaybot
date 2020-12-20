import os, jwt, time
from models.user import user

class auth():
    algorithm = 'HS256'
    secret    = os.getenv('JWT_SECRET') if os.getenv('JWT_SECRET') else "ThisIsNotASecret"
    ttl       = int(os.getenv('TOKEN_TTL')) if os.getenv('TOKEN_TTL') else 86400

    def user_from_token(self, token):
        token = self.decode_token(token)
        if not token:
            return False
        if not self.verify_token(token, token['userid']):
            return False
        return user.get(token['userid'])

    def token(self, userid):
        encoded_jwt = jwt.encode(self.default_token({'userid': userid}), self.secret, algorithm=self.algorithm).decode("utf-8")
        return encoded_jwt

    def verify_token(self, token, userid):
        if type(token) != dict:
            token = self.decode_token(token)
        if not token:
            return False
        user_valid = token['userid'] == userid
        expired    = token['created'] < time.time() - self.ttl
        return user_valid and not expired

    def userid_from_token(self, token):
        token = self.decode_token(token)
        return token['userid'] if token else False

    def decode_token(self, token):
        try:
            decoded_jwt = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except:
            return False
        return decoded_jwt

    def default_token(self, fields):
        token = {
            "created": int(time.time())
        }
        token.update(fields)
        return token
import binascii

from pyDes import des
from pyDes import CBC
from pyDes import PAD_PKCS5

class AuthController:
    def __init__(self,pk,default='000000001'):
        if pk is None:
            self.use_secret = False
        else:
            self.use_secret = True
            self.key = pk
            self.default = default
            self.iv = pk
            self.des = des(self.key,CBC,self.iv,pad=None,padmode=PAD_PKCS5)

    def __encrypt(self,raw) -> bytes:
        return binascii.b2a_hex(self.des.encrypt(raw,padmode=PAD_PKCS5))

    def __decrypt(self,se_raw) -> bytes:
        return self.des.decrypt(binascii.a2b_hex(se_raw),padmode=PAD_PKCS5)

    def get_id(self,se_id):
        if self.use_secret:
            uid = self.default
            try:
                uid = self.__decrypt(se_id).decode()
            except:
                pass
        else:
            uid = se_id
        return uid

    def generate_id(self,uid):
        if self.use_secret:
            return self.__encrypt(uid).decode()
        else:
            return uid

if __name__ == "__main__":
    import os
    uid = input("input your id > ")
    handler = AuthController(os.environ.get("auth"))
    se_id = handler.generate_id(uid)
    print(f"Secret Id : {se_id}")
    print(f"Secret Id decrypted : {handler.get_id(se_id)}")
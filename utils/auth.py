import binascii

from pyDes import des
from pyDes import CBC
from pyDes import PAD_PKCS5

class AuthController:
    def __init__(self,pk,default='000000001'):
        self.key = pk
        self.default = default
        self.iv = pk
        self.des = des(self.key,CBC,self.iv,pad=None,padmode=PAD_PKCS5)

    def __encrypt(self,raw) -> bytes:
        return binascii.b2a_hex(self.des.encrypt(raw,padmode=PAD_PKCS5))

    def __decrypt(self,se_raw) -> bytes:
        return self.des.decrypt(binascii.a2b_hex(se_raw),padmode=PAD_PKCS5)

    def get_id(self,se_id):
        uid = self.default
        try:
            uid = self.__decrypt(se_id).decode()
        except:
            pass
        return uid

    def generate_id(self,uid):
        return self.__encrypt(uid).decode()

if __name__ == "__main__":
    import os
    uid = input("input your id > ")
    handler = AuthController(os.environ.get("auth","mHAcxLYz"))
    se_id = handler.generate_id(uid)
    print(f"Secret Id : {se_id}")
    print(f"Secret Id decrypted : {handler.get_id(se_id)}")
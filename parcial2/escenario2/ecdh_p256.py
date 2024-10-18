from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Protocol.DH import key_agreement

class ECDH_P256:

    def __init__(self):
        self.generate_new_keys()

    def generate_new_keys(self):
        self.privateKey = ECC.generate(curve='P-256')
        self.publicKey = self.privateKey.public_key()
    
    def get_simetric_key(self, encoded_public_key):

        public_key = ECC.import_key(encoded_public_key)

        def KDF(input_data):
            hash_object = SHA256.new()
            hash_object.update(input_data)
            return hash_object.digest()

        session_key = key_agreement(static_priv=self.privateKey, static_pub=public_key, kdf=KDF)

        return session_key


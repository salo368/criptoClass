from __future__ import annotations

import json
from pprint import pformat

from Crypto.Random.random import randint

class DiffieHellmanProtocol:

    def __init__(self, p: int, q: int, g: int):
        self.p = p
        self.q = q
        self.g = g
        self.sk = self.__gen_secret_key() # Llave secreta aleatoria [1, q-2]
        self.pk = self.__get_public_key() # Llave publica g^α mod p

    def __gen_secret_key(self) -> int:
        private_key = randint(1, self.q - 2)
        return private_key
    
    def __get_public_key(self) -> int:
        public_key = pow(self.g, self.sk, self.p)
        return public_key

    def get_shared_secret(self, others_pk: int) -> int:
        shared_secret = pow(others_pk, self.sk, self.p)
        return shared_secret
    
    def to_json(self) -> str:
        variables = vars(self).copy()
        del variables["sk"]
        return json.dumps(variables)

    def __bytes__(self) -> bytes:
        return self.to_json().encode()

    def __str__(self) -> str:
        return pformat(vars(self), width=400, sort_dicts=False)
    
    @classmethod
    def from_json(cls, params_pk) -> DiffieHellmanProtocol:
        params = json.loads(params_pk)
        params.pop("pk", None)
        return cls(**params)

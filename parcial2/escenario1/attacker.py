import math
import time
from salsa import Salsa20Cipher

def PasoDeBebePasoDeGigante(g: int, y: int, n: int) -> int:
    # Calculamos m, que será el tamaño de los pasos (baby steps y giant steps)
    # Lo definimos como el techo de la raíz cuadrada de n
    m = math.ceil(math.sqrt(n))

    # Creamos un diccionario para almacenar los "baby steps"
    # Aquí guardaremos las potencias de g^j (mod n) para valores de j entre 0 y m-1
    gamma = {}

    # Baby step: computamos g^j para j = 0, 1, ..., m-1
    # Estas potencias se almacenan en el diccionario gamma, donde la clave es g^j % n
    # y el valor asociado es j (el exponente)
    for j in range(m):
        gamma[pow(g, j, n)] = j

    # Calculamos beta = g^(-m) (mod n), que será utilizado en los "giant steps"
    # Este valor es necesario porque nos permite ir dando saltos grandes en las potencias de g
    beta = pow(g, -m, n)

    # Inicializamos ipsilon como y, este será el valor que iremos comparando con los baby steps
    ipsilon = y

    # Giant step: iteramos sobre i desde 0 hasta m-1 para encontrar una coincidencia
    # entre el valor de y * beta^i y uno de los valores de g^j precomputados en los baby steps
    for i in range(m):

        # Si el valor actual de ipsilon está en el diccionario gamma (es decir, coincide con
        # algún g^j mod n calculado previamente en los baby steps), entonces hemos encontrado una solución
        if ipsilon in gamma:
            # Si encontramos la coincidencia, el valor de x se calcula como:
            # x = i * m + j, donde j es el valor guardado en gamma
            x = i * m + gamma[ipsilon]
            break
        
        # Si no encontramos una coincidencia, actualizamos ipsilon para el siguiente giant step:
        # ipsilon = ipsilon * beta (mod n)
        ipsilon = (ipsilon * beta) % n

    # Devolvemos x, que es el exponente tal que g^x ≡ y (mod n)
    return x

def main(p: int, g: int, server_pk: int, client_pk: int, messages: list[str]):
    start = time.perf_counter()
    server_sk = PasoDeBebePasoDeGigante(g, y=server_pk, n=p)
    elapsed  = time.perf_counter() - start
    print(f"Time taken: {elapsed:.6f} seconds")

    print("Server sk:", server_sk)

    shared_secret = pow(client_pk, server_sk, p)
    print("Shared secret:", shared_secret)

    salsa = Salsa20Cipher()
    salsa.key = str(shared_secret).encode()
    print("Symmetric key:", salsa)

    for i, encrypted_message in enumerate(messages):
        decrypted_message = salsa.decrypt(bytes.fromhex(encrypted_message)).decode()
        print(f"message {i}:", decrypted_message)


if __name__ == "__main__":
    cases = {
        "case 1": {
            "p": 227,
            "g": 12,
            "server_pk": 75,
            "client_pk": 177,
            "messages": ["e262c4525b8dce23d9", "426c0878144046a7b7", "1f35db6398422086e9"]
        },
        "case 2": {
            "p": 51047,
            "g": 93,
            "server_pk": 2873,
            "client_pk": 1441,
            "messages": ["c1c9eeb8f4c76408fa", "0294a1a247b998b140", "e06035c688d579b981"]
        },
        "case 3": {
            "p": 14330819,
            "g": 1970788,
            "server_pk": 1202224,
            "client_pk": 4401904,
            "messages": ["2a6e53806077918d22", "ae8b14ed6790f4b71b", "458b7d7a7123c2f254"]
        }
    }

    for i, case in cases.items():
        print(i)
        main(**case)
        print()

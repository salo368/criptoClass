from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from Crypto.Math._IntegerCustom import IntegerCustom
import random
import math

class elGamalCipher:

    def __init__(self):
        self.private_key = 56459588155347625603076788246988333206337585740834995204479895449303912072570919145837195952098055737525819181950631566981749366400796700407151622822124801426775783957104229906668656889376804172177688066252709768909151170515000213771092112754659127387887424656217035013857411046459092612923724828857419854092#int(key.x)  
        self.public_key = 35890631159686991535428322594001386513710103692201632981546694462138807525758408055192393853650751880608912553387686395925903690223888114502215299335236409253823992994943533432127700761505269985496504356471178537314223495435883283338159486823375953038283468032491985831661457893917605998541757330807820528872#int(key.y)   
        self.p = 143298756574985216105180427405795645721541229169601176251232326260349524776653562187605417180724290051915981034064908439243465352683202880446774623933843347537595724179016718849890362805603949377260893517125396004838427250285078457594131435294923634066464581353028593345397958220981758038594102785557044521743#int(key.p)           
        self.g = 63762161597153363042977925135432951570395101302484449400396611424039446580601770257495490211506135462197377247692142092241101053345770688278677254358443491235329074490875799787587045080724012153749189586891533221391235672541976394343014832031061820110802326315580958571563903032789843904761123355848048503010#int(key.g)            
        self.block_size = (self.p.bit_length() + 7) // 8 
        # key = ElGamal.generate(512, get_random_bytes)
        # self.private_key = int(key.x)  
        # self.public_key = int(key.y)   
        # self.p = int(key.p)           
        # self.g = int(key.g)            

    def encrypt(self, data: bytes, public_key, p, g) -> bytes:
        m = IntegerCustom(int.from_bytes(data, 'big'))  
        
        blocks = []
        while m >= p:
            blocks.append(m % p)
            m = m // p
        blocks.append(m)
        blocks = blocks[::-1]  

        encrypted_bytes = bytearray()
        for block in blocks:
            k = random.randint(1, p - 1)
            while math.gcd(k, p) != 1:
                k = random.randint(1, p - 1)

            v = pow(g, k, p)
            w = pow(public_key, k, p)
            c = (block * w) % p

            encrypted_bytes.extend(c.to_bytes(self.block_size, 'big'))
            encrypted_bytes.extend(v.to_bytes(self.block_size, 'big'))
        
        return bytes(encrypted_bytes)
            
    def decrypt(self, encrypted_data: bytes) -> bytes:
        encrypted_blocks = []
        
        for i in range(0, len(encrypted_data), 2 * self.block_size):
            c = int.from_bytes(encrypted_data[i:i + self.block_size], 'big')
            v = int.from_bytes(encrypted_data[i + self.block_size:i + 2 * self.block_size], 'big')
            encrypted_blocks.append((c, v))

        decrypted_blocks = []
        for c, v in encrypted_blocks:    
            w = pow(v, self.private_key, self.p)  
            w_inv = pow(w, self.p - 2, self.p)    
            m = (c * w_inv) % self.p
            decrypted_blocks.append(m)
        
        m_total = IntegerCustom(0)
        for block in decrypted_blocks:
            m_total = m_total * self.p + block
        
        m_int = m_total._value
        return m_int.to_bytes((m_int.bit_length() + 7) // 8, 'big')



# ALICE = elGamalCipher()
# BOB = elGamalCipher()

# bob_public_key = BOB.public_key
# bob_p = BOB.p
# bob_g = BOB.g
# alice_public_key = ALICE.public_key



# texto = 'La creatividad es una de las capacidades humanas más valiosas, y su influencia se extiende a prácticamente todos los ámbitos de la vida. A menudo asociada con las artes, la creatividad es en realidad un pilar fundamental en el desarrollo de cualquier disciplina, desde la ingeniería hasta la ciencia, pasando por los negocios y la educación. En un mundo cada vez más competitivo y globalizado, la creatividad ha dejado de ser solo una ventaja; se ha convertido en una necesidad para quienes buscan destacar y generar un impacto duradero.'
# enc = ALICE.encrypt(texto.encode(), bob_public_key, bob_p, bob_g)

# mensage = BOB.decrypt(enc)
# print(mensage.decode())




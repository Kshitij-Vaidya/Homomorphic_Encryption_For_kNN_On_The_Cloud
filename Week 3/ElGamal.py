import random

def extended_euclidean_algorithm(a, b):
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_euclidean_algorithm(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


def inverse_of(n, p):
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd
    if gcd != 1:
        raise ValueError("Has no multiplicative inverse")
    else:
        return x % p


class ElGamal:
    def __init__(self, g, p):
        self.g = g
        self.p = p  # g is the generator of the cyclic group Z_p* and p is the prime whose cyclic group we consider
        self.x = random.randint(1, p - 1)  # Here x is the private key generated
        self.h = pow(self.g, self.x, self.p)
        self.y = None
        self.c1 = None

    def get_public_key(self):
        return self.p, self.g, self.h

    def encrypt(self, plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')
        if plaintext_int >= self.p:
            raise ValueError("Message too large for encryption")
        p, g, h = self.get_public_key()
        print(f"Generator: {g}")
        print(f"Prime: {p}")
        # print(f"Private key: {self.x}")
        print(f"h = {self.h}")
        self.y = random.randint(1, p - 1)
        s = pow(h, self.y, p)  # This is called the shared secret
        self.c1 = pow(g, self.y, p)
        cipher = (plaintext_int * s) % p  # This is the ciphertext
        cipher_bytes = cipher.to_bytes((cipher.bit_length()+7)//8, 'big')
        return cipher_bytes

    def decrypt(self, ciphertext):
        ciphertext_bytes = int.from_bytes(ciphertext, 'big')
        if ciphertext_bytes >= self.p:
            raise ValueError("Ciphertext too large to be decoded")
        s1 = pow(self.c1, self.x, self.p)  # This secret must be the same as the shared secret used while encryption
        s_inverse = inverse_of(s1, self.p)  # Computes the inverse of s1 modulo p
        message = (ciphertext_bytes * s_inverse) % self.p
        message_bytes = message.to_bytes((message.bit_length()+7)//8, 'big')
        return message_bytes


test1 = ElGamal(6059056325654647085094673182820944702832808469246997590718614195302008976987677315330071892238115498233312708495024254444096787664043222683347160040706719286459263151857138107380333342113325579387780454681519176118730887918867537162514761997437249443, 7987903360290893870380841504510894449635092976012306005418780150883535078584661327124984048104946827664497045936791187482354329085853313906411064846262914819364089011651321400398782595157593889738511521280352222376627915193982566811045451019495202587)
m = b"5"
print(f"Message: {m}")
e_m = test1.encrypt(m)
print(f"Encrypted message: {e_m}")
d_m = test1.decrypt(e_m)
print(f"Decrypted message: {d_m}")

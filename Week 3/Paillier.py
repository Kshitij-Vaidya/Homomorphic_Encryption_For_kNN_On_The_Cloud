# Large Prime Generation for RSA
import random

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def nBitRandom(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def getLowLevelPrime(n):
    while True:
        # Obtain a random number
        pc = nBitRandom(n)

        # Test divisibility by pre-generated
        # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
                break
        else:
            return pc


def isMillerRabinPassed(mrc):
    maxDivisionsByTwo = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert (2 ** maxDivisionsByTwo * ec == mrc - 1)

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True


def main(n):
    while True:
        # n = 1024
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate


def gcd(a, b):
    # Calculate the greatest common divisor (GCD) using Euclidean algorithm
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    # Calculate the LCM using the formula: LCM(a, b) = (a * b) / GCD(a, b)
    return (a * b) // gcd(a, b)


def has_modular_inverse(a, modulus):
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, X, y = extended_gcd(b, a % b)
        return gcd, y, X - (a // b) * y

    gcd, x, _ = extended_gcd(a, modulus)
    if gcd == 1:
        return True
    else:
        return False


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


class Paillier:
    def __init__(self, k):
        self.p = main(k)
        self.q = main(k)  # Generate 2 k-bit prime numbers
        while self.p == self.q:
            self.p = main(k)
            self.q = main(k)

        self.N = self.p * self.q
        self.gL = lcm(self.p - 1, self.q - 1)
        self.g = random.randint(1, self.N ** 2)
        while not gcd(self.g, self.N ** 2):
            self.g = random.randint(1, self.N ** 2)

        self.L = (pow(self.g, self.gL, self.N ** 2) - 1) // self.N
        self.gMU = inverse_of(self.L, self.N)
        self.L1 = None

        # Public key: (N, g)
        # Private key: (L, gMu)

    def get_public_key(self):
        print(f"Public Key: {self.N} {self.g}")
        return self.N, self.g

    def encrypt(self, plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')
        k1 = pow(self.g, plaintext_int, self.N ** 2)
        r = random.randint(1, self.N)
        while not gcd(r, self.N) == 1:
            r = random.randint(1, self.N)
        k2 = pow(r, self.N, self.N ** 2)

        cipher = (k1 * k2) % (self.N ** 2)
        cipher_bytes = cipher.to_bytes((cipher.bit_length()+7)//8, 'big')
        return cipher_bytes

    def decrypt(self, ciphertext):
        ciphertext_int = int.from_bytes(ciphertext, 'big')
        self.L1 = (pow(ciphertext_int, self.gL, self.N ** 2) - 1) // self.N
        mess = (self.L1 * self.gMU) % self.N
        mess_bytes = mess.to_bytes((mess.bit_length() + 7) // 8, 'big')
        return mess_bytes


test = Paillier(k=32)
n, g = test.get_public_key()
# print(f"Private Key: {test.L}, {test.gMU}")
message = b"Hello"
print(message)
encrypted = test.encrypt(message)
print(encrypted)
decrypted = test.decrypt(encrypted)
print(decrypted)

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


class RSA:
    def __init__(self, k, e=65537):
        self.k = k
        self.e = e
        self.p = main(self.k)
        self.q = main(self.k)
        while self.p == self.q:
            self.p = main(self.k)
            self.q = main(self.k)
        self.N = self.p * self.q
        self.L = lcm(self.p - 1, self.q - 1)
        self.d = None

    def get_public_key(self):
        print(f"Public Key: {self.N},{self.e}")
        return self.N, self.e

    def encrypt(self, plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')
        if plaintext_int >= self.N:
            raise ValueError("Plaintext too large for encryption")
        M = pow(plaintext_int, self.e, self.N)
        M_bytes = M.to_bytes((M.bit_length()+7)//8, 'big')
        return M_bytes

    def decrypt(self, ciphertext):
        ciphertext_int = int.from_bytes(ciphertext, 'big')
        self.d = inverse_of(self.e, self.L)  # Private key exponent
        if ciphertext_int >= self.N:
            raise ValueError("Ciphertext too large for decryption")
        m = pow(ciphertext_int, self.d, self.N)
        m_bytes = m.to_bytes((m.bit_length()+7)//8, 'big')
        return m_bytes


test1 = RSA(k=1024)
message = b"Hello"
test1.get_public_key()
encrypted_message = test1.encrypt(message)
print(f"Message: {message}")
print(f"Encrypted Message: {encrypted_message}")
decrypted_message = test1.decrypt(encrypted_message)
print(f"Decrypted Message: {decrypted_message}")


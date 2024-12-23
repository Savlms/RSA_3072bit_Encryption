import random
import sys

sys.setrecursionlimit(1000000)  # This was introduced to increase recursion limit for large primes


# Extended Euclidean Algorithm for modular inverse
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


# Modular inverse function
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m


# Using Miller-Rabin primality test
def is_probably_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Prime number generation
def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if is_probably_prime(p):
            return p


# RSA Key Generation
def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g, _, y = egcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g, _, y = egcd(e, phi)
    d = modinv(e, phi)
    return (e, n), (d, n)


# RSA Encryption
def encrypt(plaintext, public_key):
    key, n = public_key
    return [pow(ord(char), key, n) for char in plaintext]


# RSA Decryption
def decrypt(ciphertext, private_key):
    key, n = private_key
    return ''.join([chr(pow(char, key, n)) for char in ciphertext])


# Example usage
if __name__ == "__main__":
    message = "The quick brown fox jumps over the lazy dog."
    print("Original message:", message)

    # Generate RSA public and private keys (3072-bit)
    public_key, private_key = generate_keypair(3072)
    print("Public key:", public_key)
    print("Private key:", private_key)

    # Encrypt the message using the public key
    encrypted = encrypt(message, public_key)
    print("Encrypted message:", encrypted)

    # Decrypt the message using the private key
    decrypted = decrypt(encrypted, private_key)
    print("Decrypted message:", decrypted)

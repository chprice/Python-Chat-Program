from util.encryption import *
import random
class Encryptor(object):

    def __init__(self, secret_key=None):
        self.secret_key = None

    def set_key(self, secret_key):
        self.secret_key = secret_key

    def encrypt(self, message):
        return numeric_encrypt(message, self.secret_key).encode()

    def decrypt(self, message):
        return binary_to_string(numeric_encrypt(message.decode(), self.secret_key))

    def generate_new_diffie_hellman_set(self):
        prime = random.randint(1000, 9000)
        while not isPrime(prime):
            prime = random.randint(1000, 9000)
        base = random.randint(20, 100)
        a = random.randint(20, 100)
        return (prime, base, a)
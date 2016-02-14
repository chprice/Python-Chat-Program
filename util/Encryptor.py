import random, math


class Encryptor(object):

    def __init__(self, secret_key=None):
        self.secret_key = None

    def set_key(self, secret_key):
        self.secret_key = secret_key

    def encrypt(self, message):
        return self._numeric_encrypt(message, self.secret_key).encode()

    def decrypt(self, message):
        return self._binary_to_string(self._numeric_encrypt(message.decode(), self.secret_key))

    def generate_new_diffie_hellman_set(self):
        prime = random.randint(1000, 9000)
        while not self._is_prime(prime):
            prime = random.randint(1000, 9000)
        base = random.randint(20, 100)
        a = random.randint(20, 100)
        return (prime, base, a)

    # def _string_to_binary(word):
    #     """Converts the string into binary."""
    #     master = ""
    #     for letter in word:
    #         temp = bin(ord(letter))[2:]
    #         while len(temp) < 7:
    #             temp = '0' + temp
    #         master = master + temp
    #     return master

    def _pad(phrase, pad_phrase, padded_length):
        return ''.join([pad_phrase for x in xrange(padded_length-len(phrase))]) + phrase

    def _string_to_binary(word):
        return ''.join([_pad(bin(ord(letter))[2:], '0', 7) for letter in word])

    def _binary_encrypt(self, message, key):
        """Encrypts the binary message by the binary key."""
        count = 0
        master = ""
        for letter in message:
            if count == len(key):
                count = 0
            master += str(int(letter) ^ int(key[count]))
            count += 1
        return master

    def _numeric_encrypt(self, str, number):
        """Encrypts the string by the number."""
        return self._binary_encrypt(self._string_to_binary(str), bin(number)[2:])

    def _binary_to_string(self, binary):
        """Returns the string representation of the binary.
        Has trouble with spaces.

        """
        master = ""
        for x in range(0, int(len(binary) / 7)):
            master += chr(int(binary[x * 7: (x + 1) * 7], 2) + 0)
        return master

    def _is_prime(self, number):
        """Checks to see if a number is prime."""
        x = 1
        while x < math.sqrt(number):
            x += 1
            if number % x == 0:
                return False
        return True

    def _is_prime_helper(self, number):
        return [number % x == 0 for x in range(int(math.sqrt(number)))]
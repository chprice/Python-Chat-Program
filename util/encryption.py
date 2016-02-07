import math

def string_to_binary(word):
    """Converts the string into binary."""
    master = ""
    for letter in word:
        temp = bin(ord(letter))[2:]
        while len(temp) < 7:
            temp = '0' + temp
        master = master + temp
    return master

def binary_encrypt(message, key):
    """Encrypts the binary message by the binary key."""
    count = 0
    master = ""
    for letter in message:
        if count == len(key):
            count = 0
        master += str(int(letter) ^ int(key[count]))
        count += 1
    return master

def numeric_encrypt(string, number):
    """Encrypts the string by the number."""
    return binary_encrypt(string_to_binary(string), bin(number)[2:])

def binary_to_string( binary):
    """Returns the string representation of the binary.
    Has trouble with spaces.

    """
    master = ""
    for x in range(0, int(len(binary) / 7)):
        master += chr(int(binary[x * 7: (x + 1) * 7], 2) + 0)
    return master

def isPrime(number):
    """Checks to see if a number is prime."""
    x = 1
    if number == 2 or number == 3:
        return True
    while x < math.sqrt(number):
        x += 1
        if number % x == 0:
            return False
    return True
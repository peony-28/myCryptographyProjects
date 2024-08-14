import random

class RSA:
    def __init__(self, bit_length=8):
        self.bit_length = bit_length
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        while self.q == self.p:
            self.q = self.generate_prime()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.find_e(self.phi)
        self.d = self.mod_inverse(self.e, self.phi)
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    def generate_prime(self):
        while True:
            num = random.getrandbits(self.bit_length)
            if num % 2 == 0:
                continue
            if self.is_probable_prime(num):
                return num

    def is_probable_prime(self, num, k=5):
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        r = num - 1
        s = 0
        while r % 2 == 0:
            r //= 2
            s += 1
        for _ in range(k):
            a = random.randint(2, num - 2)
            x = pow(a, r, num)
            if x == 1 or x == num - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, num)
                if x == num - 1:
                    break
            else:
                return False
        return True

    def find_e(self, phi):
        e = 3
        while self.gcd(e, phi) != 1:
            e += 2
        return e

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def mod_inverse(self, e, phi):
        g, x, y = self.extended_gcd(e, phi)
        if g != 1:
            raise ValueError("Modular inverse does not exist")
        else:
            return x % phi

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def encrypt(self, message, public_key):
        e, n = public_key
        cipher = [pow(ord(char), e, n) for char in message]
        return cipher

    def decrypt(self, cipher, private_key):
        d, n = private_key
        plain = [chr(pow(char, d, n)) for char in cipher]
        return ''.join(plain)
    
    def show_keys(self):
        
        print("Generated Prime p: ",self.p)
        print("Generated Prime q: ", self.q)
        
        print("Public Key (e, n):", self.public_key)
        print("Private Key (d, n):", self.private_key)

if __name__ == "__main__":
    rsa = RSA()
    rsa.show_keys()
    
    message = "Hello there!"
    print("The original message:" + message)
    encrypted_message = rsa.encrypt(message, rsa.public_key)
    print("\nEncrypted Message:", encrypted_message)

    decrypted_message = rsa.decrypt(encrypted_message, rsa.private_key)
    print("\nDecrypted Message:", decrypted_message)

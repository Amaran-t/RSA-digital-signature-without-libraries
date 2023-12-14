import random
import hashlib

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def is_prime(num, test_count=10):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0:
        return False

    s, d = 0, num - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2

    for _ in range(test_count):
        a = random.randint(2, num - 2)
        x = pow(a, d, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

def generate_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Экспонента (по стандарту RSA)
    d = modinv(e, phi)
    return ((e, n), (d, n))

def sign(message, private_key):
    e, n = private_key
    hashed_message = hashlib.sha256(message.encode()).digest()
    signature = pow(int.from_bytes(hashed_message, byteorder='big'), e, n)
    return signature

def verify(message, signature, public_key):
    e, n = public_key
    hashed_message = hashlib.sha256(message.encode()).digest()
    decrypted_signature = pow(signature, e, n)
    return int.from_bytes(hashed_message, byteorder='big') == decrypted_signature

if __name__ == "__main__":
    bits = 2048  # Размер ключа (можете изменить на 1024 или другой, но больший более безопасен)
    message = "Hello, world!"

    public_key, private_key = generate_keypair(bits)

    signature = sign(message, private_key)
    print("Подпись:", signature)

    if verify(message, signature, public_key):
        print("Подпись верна. Сообщение не было изменено.")
    else:
        print("Подпись недействительна. Сообщение было изменено или ключи не совпадают.")

from secrets import SystemRandom
import secrets
import random
import math
import sys

sys.setrecursionlimit(1500)

def two_factors(n):
    r = 0
    while n % 2 == 0:
        n //= 2
        r += 1
    return r, n

def miller_rabin(n, k=5):
    if n <= 1:
        return False

    if n <= 3:
        return True

    r, d = two_factors(n - 1)

    if (2 ** r) * d + 1 != n:
        print("2^r * d + 1 != n")
        exit()
    if d % 2 == 0:
        print("d não é ímpar")
        exit()

    for _ in range(k):
        rand_num = random.randint(2, n - 2)
        x = pow(rand_num, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = (x ** 2) % n

        if x == n - 1:
            continue
        return False

    return True

def generate_key(length=1024):
    key = ''
    flag = False

    while flag is False:
        key = secrets.randbits(length)
        flag = miller_rabin(key, 10)

    return key

def generate_e(phi):
    while True:
        e = secrets.randbelow(phi)
        if math.gcd(phi, e) == 1:
            return e

def generate_d(e, max_value):
    return modular_inversion(e, max_value)[1] % max_value

def modular_inversion(e, max_value):
    if e == 0:
        return (max_value, 0, 1)
    else:
        a, b, c = modular_inversion(max_value % e, e)
        return (a, c - (max_value // e) * b, b)

def generate_private_and_public_key():
    p = generate_key()
    q = generate_key()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = generate_e(phi)
    d = generate_d(e, phi)

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key
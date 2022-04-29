import string
import random
import binascii

r = 'abcdef'
sequence_names = []


def sequence_name_generator():
    r = 'abcdef'
    a = ""
    for i in range(0, 36):
        if i == 8 or i == 13 or i == 18 or i == 23:
            a += "-"
        else:
            b = random.choice(r + string.digits)
            a += b.lower()
    print(a)
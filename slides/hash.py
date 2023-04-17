import struct
import pandas as pd
import random


def float_to_bits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]


def hash_code(s, shift):
    mask = 0xffffffff # limit to 32-bit integers
    h = 0
    for character in s:
        h = (h << shift & mask) | (h >> (32- shift)) # 5-bit cyclic shift of running sum
        h += ord(character) # add in value of next character
    return h


def dataset():
    words = set()
    with open('pg100.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        words = set(text.split())
        print(len(words))

    with open('words.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(words))


def read_dataset():
    words = []
    with open('words.txt', 'r', encoding='utf-8') as file:
        for line in file:
            words.append(line.strip())
    return words


def frequency(words):
    freq = {}
    for word in words:
        if word in freq:
            freq[word] = freq[word] + 1
        else:
            freq[word] = 1
    return freq


def test_codes():
    for shift in range(17):
        codes = []
        for word in words:
            codes.append(hash_code(word, shift))
        freq = frequency(codes).values()
        print('Shift: ', shift)
        print(max(freq))
        print(sum(freq) - len(freq))

    codes = []
    for word in words:
        codes.append(hash(word))
    freq = frequency(codes).values()
    print(max(freq))
    print(sum(freq) - len(freq))


def division(codes, n):
    return [code % n for code in codes]


def mad(codes, n, p):
    a = random.randrange(p)
    b = random.randrange(p)
    return [((code * a + b) % p) % n for code in codes]


words = read_dataset()
print(len(words))
codes = []
for word in words:
    codes.append(hash_code(word, 5))

n = 1001
codes1 = division(codes, n)
freq = frequency(codes1).values()
print(max(freq))
print(sum(freq) - len(freq))

n = 1000
p = 1610612741
codes = mad(codes, n, p)
freq = frequency(codes).values()
print(max(freq))
print(sum(freq) - len(freq))


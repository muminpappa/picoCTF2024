def generator(g, x, p):
    return pow(g, x) % p


def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text


def decrypt(ciphertext, key):
    plaintext = ""
    for n in ciphertext:
        plaintext += chr(n // (key*311))
    return plaintext


def test():
    ciphertext = [33588, 276168, 261240, 302292, 343344, 328416, 242580, 85836, 82104, 156744, 0, 309756, 78372, 18660, 253776, 0, 82104, 320952, 3732, 231384, 89568, 100764, 22392, 22392, 63444, 22392, 97032, 190332, 119424, 182868, 97032, 26124, 44784, 63444]
    text_key = "trudeau"
    p = 97
    g = 31
    a = 89
    b = 27
    u = generator(g, a, p)
    v = generator(g, b, p)
    key = generator(v, a, p)
    b_key = generator(u, b, p)
    shared_key = None
    if key == b_key:
        shared_key = key
    else:
        print("Invalid key")

    semi_cipher = decrypt(ciphertext, shared_key)
    plaintext = dynamic_xor_encrypt(semi_cipher[::-1], text_key)
    print(plaintext[::-1])

if __name__ == "__main__":
    test()

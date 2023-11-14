import hashlib
from Key import generate_key

def integer_to_octet_string(integer, size = 4):
    return integer.to_bytes(size, "big")

def rsa_cipher_decipher(message, EorD, n):
    return pow(message, EorD, n)

def mask_generation_function(input_string, output_length, hash_func = hashlib.sha3_256):
    counter = 0
    output = b""
    while len(output) < output_length:
        counter_octets = integer_to_octet_string(counter, 4)
        output += hash_func(input_string + counter_octets).digest()
        counter += 1
    return output[:output_length]

def xor_bytes(a, b):
    return bytes(c ^ d for c, d in zip(a, b))

def oaep_cipher(public_key, message, seed = generate_key(256), label = ''):
    seed_bytes = seed.to_bytes(32, "big")
    message_bytes = bytes(message, 'utf-8')

    hash_length = 32
    message_length = len(message)
    key_length = public_key[0].bit_length() // 8

    label_hash = hashlib.sha3_256(label.encode()).digest()
    padding_ps = int.to_bytes(0, key_length - message_length - 2 * hash_length - 2, 'big')
    db = label_hash + padding_ps + b'\x01' + message_bytes
    db_mask = mask_generation_function(seed_bytes, key_length - hash_length - 1)
    masked_db = xor_bytes(db, db_mask)
    seed_mask = mask_generation_function(masked_db, hash_length)
    masked_seed = xor_bytes(seed_bytes, seed_mask)
    em = b'\x00' + masked_seed + masked_db

    em = rsa_cipher_decipher(int.from_bytes(em, 'big'), public_key[1], public_key[0])

    return em

def oaep_decipher(private_key, cryptogram , label = ""):
    hash_length = 32
    n = private_key[0].bit_length() // 8

    decrypted_message = rsa_cipher_decipher(cryptogram, private_key[1], private_key[0]).to_bytes(n, 'big')
    masked_seed = decrypted_message[1:hash_length + 1]
    masked_db = decrypted_message[-(n - hash_length - 1):]

    seed_mask = mask_generation_function(masked_db, hash_length)
    seed = xor_bytes(masked_seed, seed_mask)
    db_mask = mask_generation_function(seed, n - hash_length - 1)
    db = xor_bytes(masked_db, db_mask)
    
    message_padding = db[hash_length:]

    byte_one_found = False
    for i, byte in enumerate(message_padding):
        if byte == 1:
            byte_one_found = True
            break
    
    message = message_padding[i + 1:].decode('utf-8')

    label_hash = hashlib.sha3_256(label.encode()).digest()
    db_hash = db[:hash_length]

    if decrypted_message[0] != 0: 
        print('A mensagem encontrada não se inicia com 0x00')
        exit()
    if not byte_one_found: 
        print('O byte 0x01 não foi encontrado entre ps e a mensagem')
        exit()
    if label_hash != db_hash: 
        print('Os hashes são diferentes um do outro')
        exit()

    return message
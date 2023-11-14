from Key import generate_private_and_public_key
from Rsa import oaep_cipher, oaep_decipher, rsa_cipher_decipher
import hashlib
import base64

def read_file_content(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"O arquivo {file_name} não pôde ser encontrado.")
        exit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar ler o arquivo {file_name}: {e}")
        exit()

def generate_keys_and_cipher(file_content):
    public_key, private_key = generate_private_and_public_key()

    print(f'Chave pública gerada:\n\tn: {public_key[0]}\n\te: {public_key[1]}\nChave privada gerada:\n\tn: {private_key[0]}\n\td: {private_key[1]}\n')

    message_ciphered = oaep_cipher(public_key, file_content)  
    print(f'Mensagem cifrada: {message_ciphered}\n')

    message_deciphered = oaep_decipher(private_key, message_ciphered)
    print(f'Mensagem decifrada: {message_deciphered}\n')

    return public_key, private_key, message_deciphered

def sign_verify_content(file_content):
    public_key, private_key = generate_private_and_public_key()
    message_hash = hashlib.sha3_256(bytes(file_content.encode())).digest()

    rsa_hash = rsa_cipher_decipher(int.from_bytes(message_hash, 'big'), private_key[1], private_key[0])
    rsa_hash = rsa_hash.to_bytes((rsa_hash.bit_length() + 7) // 8, 'big')

    signature = base64.b64encode(rsa_hash)

    print(f'Mensagem assinada: {signature}\n')

    dec_signature = base64.b64decode(signature)
    dec_signature = int.from_bytes(dec_signature, 'big')
    dec_signature = rsa_cipher_decipher(dec_signature, public_key[1], public_key[0])

    if dec_signature == int.from_bytes(message_hash, 'big'):
        print('Sucesso na verificação da assinatura')
    else:
        print('Falha na verificação da assinatura')

if __name__ == "__main__":
    file_name = input("Digite o nome do arquivo\n> ")
    file_content = read_file_content(file_name)

    public_key, private_key, message_deciphered = generate_keys_and_cipher(file_content)
    sign_verify_content(file_content)
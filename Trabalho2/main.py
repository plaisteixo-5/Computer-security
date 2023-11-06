import base64
import Utils
import AES
import hashlib
import base64
from PIL import Image

# Chaves
# 123456789012345678901234567890123456789
# 72542197177113834345371639354222255895
# 11223344556677889900112233445566778899

file_content = ''
key = ''
message_cipher = b''
ciphered_message_save_file_name = 'cipher.bin'

while True:
    
    operation = int(input("O que deseja fazer?\n\n1 - Cifrar CTR\n2 - Decifrar CTR\n3 - Encerrar programa\n> "))

    if operation == 3:
        print("Encerrando programa. Até mais!")
        break
    else:
        is_image = str(input("O arquivo a ser lido é uma imagem? (S ou N)\n> ")).lower()
        is_image = True if is_image == "s" else False

        if operation == 1:
            
            file = input("Digite o nome do arquivo\n> ")
            key = Utils.get_key()
            rounds = int(input("Digite a quantidade de rounds desejados (Caso deseje o valor default, basta digitar 0)\n> "))

            if is_image:
                with open(file, 'rb') as image_file:
                    file_content = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                with open(file, 'r') as text_file:
                    file_content = text_file.read()

            if not file_content:
                print("Erro: Ocorreu um erro ao ler o arquivo ou o mesmo não tem nenhum conteúdo para ser lido.")
                continue

            message_cipher = AES.ctr_cipher(file_content, key, rounds)
            print(f'Mensagem cifrada: {message_cipher}\nSalva no arquivo: {ciphered_message_save_file_name}')
            b64_message_encoded = base64.b64encode(message_cipher)
            with open(ciphered_message_save_file_name, "wb") as f:
                f.write(b64_message_encoded)
            
        if(operation == 2):
            ciphered_message_file_name = input("Digite o nome do arquivo que contém a mensagem a ser decifrada\n> ")
            key = Utils.get_key()
            rounds = int(input("Digite a quantidade de rounds desejados (Caso deseje o valor default, basta digitar 0)\n> "))

            with open(ciphered_message_file_name, "rb") as f:
                b64_message_decoded = f.read()
            b64_message_decoded = base64.b64decode(b64_message_decoded)
            
            message_deciphered = AES.ctr_decipher(b64_message_decoded, key, rounds)
            
            if is_image:
                image_bytes = base64.b64decode(message_deciphered)
                image_file_name = input("Digite o nome do arquivo para a imagem\n> ")

                with open(image_file_name, 'wb') as image_file:
                    image_file.write(image_bytes)
            else:
                print(message_deciphered)
        
        input()
        Utils.clear_terminal()
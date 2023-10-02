'''
Autor: Felipe Fontenele dos Santos
Matrícula: 190027622
Disciplina: Segurança Computacional
Turma: 02
'''

from VigenereCipher import VigenereCipher
from CipherAttack import CipherAttack
import os

def readFile(filePath):
    message = ''
    if not os.path.exists(filePath):
        print(f'Arquivo {filePath} não foi localizado.')
        return

    with open(filePath, encoding='utf-8') as file:
        message = file.read()

    return message


def main():
    vigenereCipher = VigenereCipher()
    attack = CipherAttack()

    while True:
        print('Escolha uma opcao:\n1 - Cifrar\n2 - Decifrar\n3 - Quebrar cifra\nOutro - Sair')
        command = int(input())

        if command == 1:
            print('Digite a mensagem a ser cifrada: ')
            message = input()

            print('Digite a chave a ser utilizada: ')
            key = input()

            print(f'A mensagem cifrada é: {vigenereCipher.encrypt_message(message, key)}')
        elif command == 2:
            print('Digite a mensagem a ser decifrada: ')
            message = input()

            print('Digite a chave a ser utilizada: ')
            key = input()

            print(f'A mensagem decifrada é: {vigenereCipher.decrypt_message(message, key)}')
        elif command == 3:
            print('Deseja ler a mensagem a ser quebrada de um arquivo texto?(s\\n):')

            if input() == 's':
                filePath = input('Digite o nome do arquivo: ')
                message = readFile(filePath)
                if message == '': continue

            else:
                print('Digite a mensagem cifrada a ser quebrada: ')
                message = input()

            print('A mensagem a ser decifrada está em português ou inglês?\n\t1 - Português\n\t2 - Inglês\nDigite sua opçâo: ')
            language = int(input())
            
            if language == 1:
                language = 'pt-BR'
            else:
                language = 'en'

            attack.break_cipher_message(message, language)
        else:
            break


main()

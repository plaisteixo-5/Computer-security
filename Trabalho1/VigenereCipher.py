from unidecode import unidecode
import re


class VigenereCipher:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def decrypt_message(self, cipher_message, key):
        return self._vigenere_cipher(cipher_message, key, mode='decrypt')

    def encrypt_message(self, message, key):
        return self._vigenere_cipher(message, key)

    def _vigenere_cipher(self, message, key, mode='encrypt'):
        message_encrypted = ''
        key_index = 0
        key_shift = 0

        message, key = self._handle_message_and_key(message, key)

        for message_letter in message:
            new_char = message_letter
            if new_char.isalpha():
                key_character = key[key_index % len(key)]

                if new_char in self.alphabet:
                    key_shift = self.alphabet.index(key_character.lower())
                    message_shift = self.alphabet.index(new_char)
                else:
                    key_shift = self.ALPHABET.index(key_character)
                    message_shift = self.ALPHABET.index(new_char)

                if mode == 'decrypt':
                    key_shift = -key_shift

                new_char = self.alphabet[(message_shift + key_shift) % 26] if new_char in self.alphabet else self.ALPHABET[(message_shift + key_shift) % 26]
                key_index += 1

            message_encrypted += new_char

        return message_encrypted

    def _handle_message_and_key(self, message, key):
        """
        Método para tornar todas as letras maiúsculas, remover acentuações e qualquer caractere especial da mensagem e da chave informada.

        Args:
            message: a mensagem a ser cifrada.
            key: chave da cifra.

        Returns:
            Mensagem e chave sem pontuações, caracteres especiais e maiúsculas.
        """
        message = unidecode(re.sub(r'[^\d\w\s,.-]', '', message))
        key = unidecode(re.sub(r'[^\w\s]', '', key))

        return message, key.upper()

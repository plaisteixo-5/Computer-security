from VigenereCipher import VigenereCipher
from unidecode import unidecode
import re
import itertools



class CipherAttack:
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    freq_port = [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78,
                 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]
    freq_eng = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025,
                2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

    def break_cipher_message(self, cipher, language='pt=BR'):
        vigenere_cipher = VigenereCipher()
        aux_cipher = cipher

        cipher = self._format_cipher(cipher)
        key_size = self.get_key_size(cipher)
        key = self.discover_key(cipher, key_size, language)

        decrypted_message = vigenere_cipher.decrypt_message(aux_cipher, key)

        print(f'Chave encontrada\n \t{key}')
        print(f'Mensagem decifrada\n \t{decrypted_message}\n')

    def get_key_size(self, cipher):
        cipher = ''.join(filter(lambda character: character in self.ALPHABET, cipher))
        factors = {}

        for i in range(len(cipher)-2):
            sequential = cipher[i:i+3]

            for j in range(i+3, len(cipher)-2):
                if cipher[j:j+3] == sequential:
                    distance = j-i
                    for k in range(2, 21):
                        if distance % k == 0:
                            if(factors.get(k)):
                                factors[k] += 1
                            else:
                                factors[k] = 1
                    break

        print(f'Tamanho chave -> fatores')

        factors = sorted(factors.items(), key=lambda x:x[1], reverse=True)
        
        for dict_factories in factors[0:3]:
            print(f'\t{dict_factories[0]} -> {dict_factories[1]}')

        print('Selecione o tamanho da chave desejada (digite 0 caso queira que o sistema decida automaticamente):')
        key_size = int(input())

        return key_size if key_size != 0 else factors[0][0]
    
    def discover_key(self, cipher, keysize, language):
        cipher = ''.join(filter(lambda character: character in self.ALPHABET, cipher))
        key = ''

        if language == 'pt-BR':
            language_frequency = self.freq_port
        else:
            language_frequency = self.freq_eng

        for i in range(keysize):
            distr = ''.join([cipher[j] for j in range(i, len(cipher), keysize)])
            index = self.frequency_analysis(distr, language_frequency)
            key += self.ALPHABET[index]

        return key

    def frequency_analysis(self, letters, language_frequency):
        frequency = self.message_frequency(letters)
        dif = []

        for _ in range(26):
            dif.append(sum([language_frequency[i]*frequency[i] for i in range(26)]))
            frequency.append(frequency.pop(0))

        return dif.index(max(dif))

    def message_frequency(self, message):
        frequency = [0] * 26
        message_length = len(message)

        for i in message:
            frequency[self.ALPHABET.find(i)] += 1

        for i in range(len(frequency)):
            if frequency[i] != 0:
                frequency[i] /= message_length

        return frequency

    def _format_message(self, message):
        message = unidecode(re.sub(r'[^\w\s.,-]', '', message))

        return message.upper()

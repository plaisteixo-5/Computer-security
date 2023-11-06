import platform
import os

def clear_terminal():
    if is_windows():
        os.system("cls")
    else:
        os.system("clear")

def is_windows():
    if platform.system() == "Linux":
        return False

    return True

def get_key():
    key = int(input("Digite o valor da chave\n> "))
        
    try:
        key.to_bytes(16, 'big')
    except:
        print("AES suporta apenas chaves de 128 bits")
        exit()

    return key
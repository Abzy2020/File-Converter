import os
from cryptography.fernet import Fernet

class FileEncryptor:

    def __init__(self, file_path):
        self.file_path = file_path
        

    def encrypt_file(self):
        #read file data
        with open(f"{self.file_path}", "rb") as file:
            b = file.read()
        #encrypt file data
        cipher = os.environ['CIPHER']
        lock = Fernet(cipher)
        encrypted_file = lock.encrypt(b)
        #write encrypted file data
        with open(f"{self.file_path}", "wb") as file:
            file.write(encrypted_file)

    
    def decrypt_file(self):
        #read file data
        with open(f"{self.file_path}", "rb") as file:
            b = file.read()
        #decrypt file data
        cipher = os.environ['CIPHER']
        unlock = Fernet(cipher)
        decrypted_file = unlock.decrypt(b)
        #write decrypted file data
        with open(f"{self.file_path}", "wb") as file:
            file.write(decrypted_file)

    
    def generate_cipher():
        key = Fernet.generate_key()
        print(key)
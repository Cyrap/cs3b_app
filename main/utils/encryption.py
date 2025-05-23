from Crypto.Cipher import AES
import base64


class Encryptor:
    def __init__(self, key):
        self.key = key[:32].ljust(32)

    def encrypt(self, plaintext):
        cipher = AES.new(self.key.encode(), AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, encrypted_text):
        data = base64.b64decode(encrypted_text.encode())
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(self.key.encode(), AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

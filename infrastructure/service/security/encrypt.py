from cryptography.fernet import Fernet

key = Fernet.generate_key()


class Encryption:

    def verify_email_encryption(self, email, uid):
        try:
            string_encryption = str(email)+","+str(uid)

            f = Fernet(key)
            token = f.encrypt(bytes(string_encryption, encoding='utf-8'))
            token = str(token, encoding='utf-8')
            return token
        except Exception as e:
            return e

    def verify_email_decryption(self, token):
        try:

            f = Fernet(key)
            token = bytes(token, encoding='utf-8')
            token = f.decrypt(token)
            string_decryption = str(token, encoding='utf-8')
            return string_decryption
        except Exception as e:
            return e

import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

class AESKey:
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_aes_key(self):
        aes_key = get_random_bytes(16)  # Gera uma chave AES de 128 bits
        print(f"Chave AES gerada: {aes_key.hex()}")  # Verifique se a chave é gerada
        return aes_key.hex()

    def save_aes_key_to_json(self):
        # Garante que o diretório exista
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        aes_key = self.generate_aes_key()

        new_key = {
            'AES_KEY': aes_key
        }

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    keys_data = json.load(file)
                except json.JSONDecodeError:
                    keys_data = []
        else:
            keys_data = []

        keys_data.append(new_key)

        with open(self.file_path, 'w') as file:
            json.dump(keys_data, file, indent=4)

        print(f"Chave AES salva em {self.file_path}")  # Confirma que a chave foi salva

    def cifrar(self, message):
        aes_key_hex = None
        
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                keys_data = json.load(file)
            if keys_data:
                aes_key_hex = keys_data[-1]['AES_KEY']

        if aes_key_hex:
            try:
                aes_key = bytes.fromhex(aes_key_hex)
                cipher = AES.new(aes_key, AES.MODE_EAX)
                nonce = cipher.nonce
                ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
                return nonce + ciphertext  # Concatena nonce e mensagem criptografada
            except Exception as e:
                print(f"Ocorreu um erro ao criptografar a mensagem: {e}")
                return None
        else:
            print("Nenhuma chave AES encontrada para criptografar a mensagem.")
            return None

    def decifrar(self, encrypted_message):
        aes_key_hex = None
        
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                keys_data = json.load(file)
            if keys_data:
                aes_key_hex = keys_data[-1]['AES_KEY']

        if aes_key_hex:
            try:
                aes_key = bytes.fromhex(aes_key_hex)
                nonce = encrypted_message[:16]  # Extrai o nonce do início da mensagem
                ciphertext = encrypted_message[16:]  # Extrai o texto criptografado
                cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
                decrypted_message = cipher.decrypt(ciphertext).decode('utf-8')
                return decrypted_message
            except Exception as e:
                print(f"Ocorreu um erro ao descriptografar a mensagem: {e}")
                return None
        else:
            print("Nenhuma chave AES encontrada para descriptografar a mensagem.")
            return None

if __name__ == "__main__":
    # Caminho do arquivo JSON onde as chaves serão armazenadas
    file_path = 'D:\\projetos\\flutter_DocuSafe\\docusafe\\aes_keys.json'
    
    aes_manager = AESKey(file_path)
    
    aes_manager.save_aes_key_to_json()

    message = "hello word"
    encrypted_message = aes_manager.cifrar(message)

    if encrypted_message:
        print(f"Mensagem criptografada: {encrypted_message}")

    decrypted_message = aes_manager.decifrar(encrypted_message)

    if decrypted_message:
        print(f"Mensagem descriptografada: {decrypted_message}")
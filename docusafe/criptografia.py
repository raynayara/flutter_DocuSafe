import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

class RSAKey:
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_rsa_keys(self):
        
        rsa_key = RSA.generate(1024)  # Gera um par de chaves RSA de 1024 bits
        private_key = rsa_key.export_key().decode('utf-8')
        public_key = rsa_key.publickey().export_key().decode('utf-8')
        return private_key, public_key

    def save_rsa_keys_to_json(self):
        
        private_key, public_key = self.generate_rsa_keys()
        
        new_key = {
            'PRIVATE_KEYRSA': private_key,
            'PUBLIC_KEYRSA': public_key
        }
        
        if os.path.exists(self.file_path):
            # Lê o conteúdo existente do arquivo JSON
            with open(self.file_path, 'r') as file:
                keys_data = json.load(file)
        else:
            keys_data = []
        
        # Adiciona a nova chave à lista
        keys_data.append(new_key)
        
        # Armazena as chaves no arquivo JSON
        with open(self.file_path, 'w') as file:
            json.dump(keys_data, file, indent=4)
    

    def cifrar(self, message):
     if os.path.exists(self.file_path):
         with open(self.file_path, 'r') as file:
             keys_data = json.load(file)
         if keys_data:
             _, public_key_str = keys_data[-1]['PRIVATE_KEYRSA'], keys_data[-1]['PUBLIC_KEYRSA']
     else:
         public_key_str = None
 
     if public_key_str:
         try:
             public_key = RSA.import_key(public_key_str)
             cipher = PKCS1_OAEP.new(public_key)
             encrypted_message = cipher.encrypt(message.encode('utf-8'))
             return encrypted_message
         except Exception as e:
             print(f"Ocorreu um erro ao criptografar a mensagem: {e}")
             return None
     return None

    def decifrar(self, encrypted_message):
     if os.path.exists(self.file_path):
         with open(self.file_path, 'r') as file:
             keys_data = json.load(file)
         if keys_data:
             private_key_str, _ = keys_data[-1]['PRIVATE_KEYRSA'], keys_data[-1]['PUBLIC_KEYRSA']
     else:
         private_key_str = None
 
     if private_key_str:
         try:
             private_key = RSA.import_key(private_key_str)
             cipher = PKCS1_OAEP.new(private_key)
             decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
             return decrypted_message
         except Exception as e:
             print(f"Ocorreu um erro ao descriptografar a mensagem: {e}")
             return None
     return None

if __name__ == "__main__":
    # Caminho do arquivo JSON onde as chaves serão armazenadas
    file_path = 'D:\\projetos\\flutter_DocuSafe\\docusafe\\keys.json'
    
    rsa_manager = RSAKey(file_path)
    
   
    # rsa_manager.save_rsa_keys_to_json()

    #message = "hello word"
    #encrypted_message = rsa_manager.cifrar(message)
    #
    #if encrypted_message:
    #    print(f"Mensagem criptografada: {encrypted_message}")
    #
    #decrypted_message = rsa_manager.decifrar(encrypted_message)
    #
    #if decrypted_message:
    #    print(f"Mensagem descriptografada: {decrypted_message}")
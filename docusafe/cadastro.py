import json
import os
import base64
from hash import hash_password
import criptografia

file_path = 'C:/Ronald/Faculdade/Seguranca/flutter_DocuSafe/docusafe/keys.json'
rsa_manager = criptografia.RSAKey(file_path)

# Nome do arquivo JSON
nome_arquivo = 'users.json'
    
def coleta_dados():
    user = input('Digite o usuário: ')
    password = input('Digite a senha: ')
    password_hashed = hash_password(password)
    return user, password_hashed

def carregar_dados_json(nome_arquivo):
    """Função auxiliar para carregar dados JSON com tratamento de erros"""
    if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 0:
        with open(nome_arquivo, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Erro ao carregar o arquivo JSON. O arquivo pode estar corrompido.")
                return None
    return {'users': []}

def cadastrar(permission):
    user, password_hashed = coleta_dados()
    
    # Criptografa a senha
    password_encrypted = rsa_manager.cifrar(password_hashed)
    
    # Converte os dados criptografados para base64 (para serem armazenados em JSON)
    password_encrypted_base64 = base64.b64encode(password_encrypted).decode('utf-8')
    
    dado = {'user': user, 'password': password_encrypted_base64, 'permissao': permission}

    # Carrega os dados JSON do arquivo
    dado_json = carregar_dados_json(nome_arquivo)

    if dado_json is None:
        # Se houver erro no arquivo JSON, inicializa os dados com uma lista vazia
        dado_json = {'users': []}

    # Verifica se o usuário já existe
    for line in dado_json.get('users', []):
        if line['user'] == user:
            print('Usuário já cadastrado')
            return

    # Adiciona o novo usuário
    dado_json['users'].append(dado)

    # Salva os dados atualizados no arquivo
    with open(nome_arquivo, 'w') as file:
        json.dump(dado_json, file, indent=4)

    print('Usuário cadastrado com sucesso')

def entrar():
    user, password_hashed = coleta_dados()
    
    # Carrega os dados JSON do arquivo
    dado_json = carregar_dados_json(nome_arquivo)
    
    if dado_json is None or not dado_json.get('users'):
        print('Usuário não cadastrado.')
        return

    # Itera sobre a lista de usuários
    for line in dado_json.get('users', []):
        if line['user'] == user:
            # Converte a senha armazenada de base64 para bytes
            password_encrypted_base64 = line['password']
            password_encrypted = base64.b64decode(password_encrypted_base64)
            
            # Descriptografa a senha
            password_decrypted = rsa_manager.decifrar(password_encrypted)
            
            if password_decrypted == password_hashed:
                print('Usuário logado com sucesso')
                return  # Encerra a função se login for bem-sucedido
            else:
                print('Senha inválida, tente novamente!')
                return entrar()
    
    print('Usuário não cadastrado. Entre em contato com um dos administradores.')

if __name__ == "__main__":
    cadastrar('adm')

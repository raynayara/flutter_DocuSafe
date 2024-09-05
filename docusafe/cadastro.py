import json
import os
from hash import hash_password

# Nome do arquivo JSON
nome_arquivo = 'users.json'
    
def coleta_dados():
    user = input('Digite o usuário: ')
    password = input('Digite a senha: ')
    password_hashed = hash_password(password)
    return user, password_hashed
def cadastrar():
    user, password_hashed = coleta_dados()
    dado = {'user': user, 'password': password_hashed}

    # Verifica se o arquivo existe e carrega os dados
    if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 0:
        with open(nome_arquivo, 'r') as file:
            dado_json = json.load(file)
            # Garante que dado_json é um dicionário com a chave 'users'
            if not isinstance(dado_json, dict):
                dado_json = {'users': []}
            if 'users' not in dado_json:
                dado_json['users'] = []
    else:
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
    
    if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 0:
        with open(nome_arquivo, 'r') as arquivo:
            dado_json = json.load(arquivo)  # Carrega o arquivo JSON
        
        # Flag para controlar se o usuário foi encontrado
        usuario_encontrado = False
        
        # Itera sobre a lista de usuários
        for line in dado_json.get('users', []):
            if line['user'] == user:
                usuario_encontrado = True  # Usuário foi encontrado
                if line['password'] == password_hashed:
                    print('Usuário logado com sucesso')
                    return  # Encerra a função se login for bem-sucedido
                else:
                    print('Senha inválida, tente novamente!')
                    return  entrar()
        
        # Se o loop terminou e o usuário não foi encontrado
        if not usuario_encontrado:
            print('Usuário não cadastrado. Entre em contato com um dos ')
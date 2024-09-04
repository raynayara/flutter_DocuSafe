import json
import os
from hash import hash_password

def cadastrar():
    user = input('Digite o usuário: ')
    password = input('Digite a senha: ')
    dado = {'user': user, 'password': hash_password(password)}

    # Nome do arquivo JSON
    nome_arquivo = 'users.json'

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
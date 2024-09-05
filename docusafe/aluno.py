import json
import os
import hashlib
from adm import carregar_dados, coleta_dados

# Caminho dos arquivos JSON
nome_arquivo_users = 'docusafe/users.json'
nome_arquivo_notas = 'docusafe/notas.json'

# Função para login do aluno
def entrar_como_aluno():
    user, password_hash = coleta_dados()

    # Verifica no arquivo users.json
    users = carregar_dados(nome_arquivo_users)
    for aluno in users.get('users', []):
        if aluno['user'] == user and aluno['password'] == password_hash:
            if aluno.get('permissao') == 'aluno':
                print(f'{aluno["user"]} logado como aluno com sucesso')
                return True, user
            else:
                print('Permissão negada. Apenas alunos podem acessar.')
                return False, None
    print('Usuário ou senha incorretos.')
    return False, None

# Função para visualizar as notas do aluno
def visualizar_notas_aluno(aluno):
    # Carregar notas do arquivo JSON
    notas = carregar_dados(nome_arquivo_notas)

    # Verifica se o aluno tem notas cadastradas
    if aluno in notas:
        print(f"\nNotas do aluno {aluno}:")
        print(f"Nota: {notas[aluno]}")
    else:
        print(f"Não há notas cadastradas para o aluno {aluno}.")

# Função principal para o fluxo do aluno
def sistema_aluno():
    sucesso, aluno = entrar_como_aluno()
    
    if sucesso:
        print(f"Bem-vindo, {aluno}!")
        
        while True:
            print("\nOpções: ")
            print("1 - Visualizar notas")
            print("0 - Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                visualizar_notas_aluno(aluno)
            elif opcao == '0':
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida, tente novamente.")

# Exemplo de execução do sistema
if __name__ == "__main__":
    sistema_aluno()

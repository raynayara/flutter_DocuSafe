import json
import os
import hashlib
from adm import carregar_dados, salvar_dados
from adm import coleta_dados
import base64
import criptografia
file_path = 'C:/Ronald/Faculdade/Seguranca/flutter_DocuSafe/docusafe/keys.json'
rsa_manager = criptografia.RSAKey(file_path)

# Função para limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Caminho do arquivo JSON
nome_arquivo_users = 'users.json'
nome_arquivo_notas = 'notas.json'

# Função para login do professor
def entrar_como_professor():
    user, password_hash = coleta_dados()

    # Verifica no arquivo users.json
    users = carregar_dados(nome_arquivo_users)
    for prof in users.get('users', []):
        if prof['user'] == user:
            password_decrypted = rsa_manager.decifrar(base64.b64decode(prof['password']))
            if password_decrypted == password_hash:
                if prof.get('permissao') == 'professor':
                    limpar_tela()
                    print(f'{prof["user"]} logado como professor com sucesso')
                    return True, user
                else:
                    print('Permissão negada. Apenas professores podem acessar.')
                    return False, None
    print('Usuário ou senha incorretos.')
    return False, None

# Função para cadastrar notas dos alunos
def cadastrar_notas_professor():
    # Carregar turmas do sistema
    users = carregar_dados(nome_arquivo_users)['users']
    alunos = [user for user in users if user.get('permissao') == 'aluno']
    
    if not alunos:
        print("Nenhum aluno cadastrado. O administrador deve cadastrar alunos.")
        return

    print("\nAlunos cadastrados")
    print("-~-"*20)
    for i, aluno in enumerate(alunos, start=1):
        print(f"{i}. {aluno['user']}")
    print("-~-"*20)
    
    boletim = {}
    for aluno in alunos:
        nota = float(input(f"Digite a nota para o aluno {aluno['user']}: "))
        boletim[aluno['user']] = nota

    # Salvar notas no arquivo JSON
    salvar_dados(nome_arquivo_notas, boletim)
    limpar_tela()
    
    print("Notas cadastradas com sucesso.")
    print("-~-"*20)
    
# Função para visualizar as turmas em que o professor leciona
def visualizar_turmas_professor(professor):
    turmas = carregar_dados('docusafe/turmas.json').get('turmas', [])
    
    turmas_professor = [turma for turma in turmas if turma['professor'] == professor]
    
    if turmas_professor:
        print(f"\nTurmas do professor {professor}:")
        for turma in turmas_professor:
            print(f"Disciplina: {turma['disciplina']}, Alunos: {', '.join(turma['alunos'])}")
    else:
        print("Você não está associado a nenhuma turma.")

# Função principal para o fluxo do professor
def sistema_professor():
    sucesso, professor = entrar_como_professor()
    
    if sucesso:
        print('\n\n')
        print(f"Bem-vindo, professor {professor}!")
        print('-~-'*20)
        while True:
            print("\nOpções: ")
            print("1 - Cadastrar notas")
            print("2 - Visualizar turmas")
            print("0 - Sair\n")
            print('-~-'*20)
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                limpar_tela()
                cadastrar_notas_professor()
            elif opcao == '2':
                limpar_tela()
                visualizar_turmas_professor(professor)
            elif opcao == '0':
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida, tente novamente.")

# Exemplo de execução do sistema
if __name__ == "__main__":
    sistema_professor()

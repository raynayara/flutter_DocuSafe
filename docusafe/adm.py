import json
import os
import hashlib

# Caminho dos arquivos JSON
nome_arquivo_users = 'docusafe/users.json'

# Função para coletar dados de login e senha
def coleta_dados():
    user = input('Digite o usuário: ')
    password = input('Digite a senha: ')
    password_hash = hashlib.sha256(password.encode()).hexdigest()  # Hash da senha
    return user, password_hash

# Função para salvar dados no arquivo JSON
def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

# Função para carregar dados do arquivo JSON
def carregar_dados(nome_arquivo):
    if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 0:
        with open(nome_arquivo, 'r') as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                print("Erro ao ler o arquivo JSON.")
                return {"users": []}
    return {"users": []}

# Função para login do administrador
def entrar_como_adm():
    user, password_hash = coleta_dados()

    # Verifica no arquivo users.json
    users = carregar_dados(nome_arquivo_users)
    for admin in users.get('users', []):
        if admin['user'] == user and admin['password'] == password_hash:
            if admin.get('permissao') == 'adm':
                print(f'{admin["user"]} logado como administrador com sucesso')
                return True
            else:
                print('Permissão negada. Apenas administradores podem acessar.')
                return False
    print('Usuário ou senha incorretos.')
    return False

# Função para salvar no arquivo 'users' com permissões
def salvar_no_users(user, password_hash, permissao):
    users = carregar_dados(nome_arquivo_users)

    if 'users' not in users:
        users['users'] = []
    
    novo_usuario = {"user": user, "password": password_hash, "permissao": permissao}
    
    users['users'].append(novo_usuario)
    salvar_dados(nome_arquivo_users, users)
    print(f'{permissao.capitalize()} {user} salvo no arquivo users com sucesso.')

# Função para cadastrar aluno
def cadastrar_aluno():
    nome_aluno = input("Digite o nome do aluno: ")
    user, password_hash = coleta_dados()  # Coleta login e senha
    salvar_no_users(user, password_hash, 'aluno')  # Salva no arquivo users com permissão de aluno

# Função para cadastrar professor
def cadastrar_professor():
    nome_professor = input("Digite o nome do professor: ")
    user, password_hash = coleta_dados()  # Coleta login e senha
    salvar_no_users(user, password_hash, 'professor')  # Salva no arquivo users com permissão de professor

# Função para cadastrar disciplina
def cadastrar_disciplina():
    nome_disciplina = input("Digite o nome da disciplina: ")
    disciplinas.append(nome_disciplina)
    print(f'Disciplina {nome_disciplina} cadastrada com sucesso.')

# Função para criar turma
def criar_turma():
    users = carregar_dados(nome_arquivo_users)['users']

    alunos = [user for user in users if user.get('permissao') == 'aluno']
    professores = [user for user in users if user.get('permissao') == 'professor']

    if not alunos or not professores or not disciplinas:
        print("É necessário cadastrar alunos, professores e disciplinas antes de criar uma turma.")
        return

    aluno = alunos[0]['user']
    professor = professores[0]['user']
    disciplina = disciplinas[0]

    turma = {
        'aluno': aluno,
        'professor': professor,
        'disciplina': disciplina
    }
    turmas.append(turma)
    print(f'Turma criada com sucesso: {turma}')

# Função para visualizar turmas
def visualizar_turmas():
    if turmas:
        for turma in turmas:
            print(f'Turma criada: {turma}')
    else:
        print('Nenhuma turma criada ainda.')

# Função principal para o fluxo do administrador
def sistema_adm():
    if entrar_como_adm():
        print("Bem-vindo, administrador!")
        
        while True:
            print("\nOpções: ")
            print("1 - Cadastrar aluno")
            print("2 - Cadastrar professor")
            print("3 - Cadastrar disciplina")
            print("4 - Criar turma")
            print("5 - Visualizar turmas")
            print("0 - Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                cadastrar_aluno()
            elif opcao == '2':
                cadastrar_professor()
            elif opcao == '3':
                cadastrar_disciplina()
            elif opcao == '4':
                criar_turma()
            elif opcao == '5':
                visualizar_turmas()
            elif opcao == '0':
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida, tente novamente.")

# Exemplo de execução do sistema
if __name__ == "__main__":
    disciplinas = []  # Inicializa lista de disciplinas
    turmas = []  # Inicializa lista de turmas
    sistema_adm()

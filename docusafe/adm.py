import json
import os
import hash
import criptografia
import base64

file_path = 'C:/Ronald/Faculdade/Seguranca/flutter_DocuSafe/docusafe/keys.json'
rsa_manager = criptografia.RSAKey(file_path)

# Caminho dos arquivos JSON
nome_arquivo_users = 'users.json'
nome_arquivo_notas = 'notas.json'

# Inicializa lista de disciplinas e turmas
disciplinas = []
turmas = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Função para coletar dados de login e senha
def coleta_dados():
    
    user = input('Digite o usuário: ')
    password = input('Digite a senha: ')
    password_hash = hash.hash_password(password) # Hash da senha
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
    user, password_hashed = coleta_dados()

    # Verifica no arquivo users.json
    users = carregar_dados(nome_arquivo_users)
    for admin in users.get('users', []):
        if admin['user'] == user:
            password_decrypted = rsa_manager.decifrar(base64.b64decode(admin['password']))
            print(password_decrypted)
            print('---------------------')
            print(password_hashed)
            if password_decrypted == password_hashed:
                if admin.get('permissao') == 'adm':
                    limpar_tela()
                    print(f'{admin["user"]} logado como administrador com sucesso')
                    print("-~-"*20)
                    
                    return True
                
                else:
                    print('Permissão negada. Apenas administradores podem acessar.')
                    return False
        print('Usuário ou senha incorretos.')
        return False

# Função para salvar no arquivo 'users' com permissões
def salvar_no_users(user, password_hashed, permissao):
    users = carregar_dados(nome_arquivo_users)

    if 'users' not in users:
        users['users'] = []
    password_encrypted = rsa_manager.cifrar(password_hashed)
    password_encrypted_base64 = base64.b64encode(password_encrypted).decode('utf-8')
    novo_usuario = {"user": user, "password": password_encrypted_base64, "permissao": permissao}
    
    users['users'].append(novo_usuario)
    salvar_dados(nome_arquivo_users, users)
    limpar_tela()
    print(f'{permissao.capitalize()} {user} cadastrado com sucesso.')

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
    limpar_tela()
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
            print("-~-"*20)
            print("1 - Cadastrar aluno")
            print("2 - Cadastrar professor")
            print("3 - Cadastrar disciplina")
            print("4 - Criar turma")
            print("5 - Visualizar turmas")
            print("0 - Sair")
            print("-~-"*20)
            
            opcao = input("Escolha uma opção: \n")
            
            if opcao == '1':
                limpar_tela()
                cadastrar_aluno()
            elif opcao == '2':
                limpar_tela()
                cadastrar_professor()
            elif opcao == '3':
                limpar_tela()
                cadastrar_disciplina()
            elif opcao == '4':
                limpar_tela()
                criar_turma()
            elif opcao == '5':
                limpar_tela()
                visualizar_turmas()
            elif opcao == '0':
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida, tente novamente.")

# Exemplo de execução do sistema
if __name__ == "__main__":
    sistema_adm()

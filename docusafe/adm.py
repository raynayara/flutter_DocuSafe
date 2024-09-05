import json
import os

# Nome do arquivo JSON para armazenar administradores
nome_arquivo_adms = 'admins.json'

# Listas globais para armazenar alunos, professores e disciplinas
alunos = []
professores = []
disciplinas = []

# Função para coletar dados de login e senha
def coleta_dados():
    user = input('Digite o usuário: ')
    password = input('Digite a senha: ')
    return user, password

# Função para login do administrador
def entrar_como_adm():
    user, password = coleta_dados()
    
    if os.path.exists(nome_arquivo_adms) and os.path.getsize(nome_arquivo_adms) > 0:
        with open(nome_arquivo_adms, 'r') as arquivo:
            try:
                dado_json = json.load(arquivo)
            except json.JSONDecodeError:
                print("Erro ao ler o arquivo JSON. Verifique se está formatado corretamente.")
                return False

        # Verifica se a chave 'admins' está presente no JSON
        if 'admins' not in dado_json:
            print("'admins' não encontrado no arquivo JSON.")
            return False

        # Verifica o login e permissões do administrador
        for admin in dado_json['admins']:
            if admin['user'] == user and admin['password'] == password:
                if admin.get('permissao') == 'adm':
                    print(f'{admin["user"]} logado como administrador com sucesso')
                    return True
                else:
                    print('Permissão negada. Apenas administradores podem acessar.')
                    return False
        print('Usuário ou senha incorretos.')
    else:
        print(f'O arquivo {nome_arquivo_adms} não foi encontrado ou está vazio.')
        return False

# Função para cadastrar aluno
def cadastrar_aluno():
    nome_aluno = input("Digite o nome do aluno: ")
    alunos.append(nome_aluno)
    print(f'Aluno {nome_aluno} cadastrado com sucesso.')

# Função para cadastrar professor
def cadastrar_professor():
    nome_professor = input("Digite o nome do professor: ")
    professores.append(nome_professor)
    print(f'Professor {nome_professor} cadastrado com sucesso.')

# Função para cadastrar disciplina
def cadastrar_disciplina():
    nome_disciplina = input("Digite o nome da disciplina: ")
    disciplinas.append(nome_disciplina)
    print(f'Disciplina {nome_disciplina} cadastrada com sucesso.')

# Função para criar turma
def criar_turma():
    if not alunos or not professores or not disciplinas:
        print("É necessário cadastrar alunos, professores e disciplinas antes de criar uma turma.")
        return
    
    turma = {
        'alunos': alunos.copy(),  # Copiando a lista para a turma
        'professor': professores[0],  # Atribui o primeiro professor cadastrado
        'disciplina': disciplinas[0]  # Atribui a primeira disciplina cadastrada
    }
    print(f'Turma criada com sucesso: {turma}')
    return turma

# Função para visualizar turmas
def visualizar_turmas(turma):
    if turma:
        print(f'Turma criada: {turma}')
    else:
        print('Nenhuma turma criada ainda.')

# Função principal para o fluxo do administrador
def sistema_adm():
    if entrar_como_adm():
        print("Bem-vindo, administrador!")
        turma = None  # Variável para armazenar a turma criada
        
        while True:
            print("\nOpções: ")
            print("1 - Cadastrar aluno")
            print("2 - Cadastrar professor")
            print("3 - Cadastrar disciplina")
            print("4 - Criar turma")
            print("5 - Visualizar turma")
            print("0 - Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                cadastrar_aluno()
            elif opcao == '2':
                cadastrar_professor()
            elif opcao == '3':
                cadastrar_disciplina()
            elif opcao == '4':
                turma = criar_turma()
            elif opcao == '5':
                visualizar_turmas(turma)
            elif opcao == '0':
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida, tente novamente.")

# Exemplo de execução do sistema
if __name__ == "__main__":
    sistema_adm()

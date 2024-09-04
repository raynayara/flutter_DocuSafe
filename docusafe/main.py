from hash import hash_password
from verificar import identifica_inutiliza

def cadastrar(username, password, user_id, role, email):
    if not identifica_inutiliza(user_id, role):
        print(f"ID não autorizado para cadastro.")
        return

    hashed_password = hash_password(password)
    try:
        with open('D:\\projetos\\flutter_DocuSafe\\docusafe\\users.txt', 'a') as file:
            file.write(f'{username},{email},{hashed_password},{role}\n')
        print(f"Usuário {username} cadastrado com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar o usuário: {e}")

def main():
    print("[1] Login")
    print("[2] Cadastro")
    option = input("Escolha uma opção: ")

    if option == '1':
        email = input('Email: ')
        password = input('Senha: ')
        
    elif option == '2':
        username = input('Nome de usuário: ')
        password = input('Senha: ')
        role = input('Função (aluno/professor/adm): ')
        email = input('Email: ')
        user_id = input('ID: ')
        cadastrar(username, password, user_id, role, email)
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
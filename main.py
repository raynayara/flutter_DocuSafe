option = input('[1] Entrar\n[2] Cadastrar')

if option == 1:
    user = input('Usuário: ')
    password = input('Senha: ')
    with open('users.txt') as file:
        for line in file:
            if f'{user} {password}' in line:
                print('Bem-vindo!')
                break
        else:
            print('Usuário ou senha inválidos')
if option == 2:
    user = input('Usuário: ')
    password = input('Senha: ')
    
    
user = input('Usuário: ')
password = input('Senha: ')

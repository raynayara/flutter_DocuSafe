def cadastrar(user, password):
    with open('users.txt', 'a') as file:
        for line in file:
            if f'{user} {password}' in line:
                print('Usuário já cadastrado')
                break
            else:
                file.write(f'{user} {password}\n')
    
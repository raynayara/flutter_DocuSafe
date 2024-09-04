import cadastro 

def app():
    option = int(input('[1] Entrar\n[2] Cadastrar'))
                
    if option == 2:
        cadastro.cadastrar()

app()
import cadastro 
from adm import sistema_adm
from prof import sistema_professor
from adm import cadastrar_aluno
from adm import cadastrar_professor
from aluno import sistema_aluno


def app():
    while True:
        print("\nBem-vindo ao sistema de gerenciamento escolar!")
        print("-~-"*20)
        option_adm = input('[1] Administrador\n[2] Professor\n[3] Aluno\n[0] Sair\n'+'-~-'*20+'\n')
        print("-~-"*20)

        if option_adm == '1':
            sistema_adm()
        elif option_adm == '2':
            sistema_professor()
        elif option_adm == '3':
            sistema_aluno()
        elif option_adm == '0':
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida, tente novamente.")
    


if __name__ == "__main__":
    app()

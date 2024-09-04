FILE_PATHS = {
    'aluno': 'D:\\projetos\\flutter_DocuSafe\\docusafe\\aluno.txt',
    'professor': 'D:\\projetos\\flutter_DocuSafe\\docusafe\\professor.txt',
    'adm': 'D:\\projetos\\flutter_DocuSafe\\docusafe\\adm.txt'
    
}



def identifica_inutiliza(id, role):
    # Obtém o caminho do arquivo baseado no papel (role)
    file_path = FILE_PATHS.get(role)
    used_ids_path = f'D:\\projetos\\flutter_DocuSafe\\docusafe\\usedid.txt'  

    try:
        # Lê os IDs do arquivo correspondente ao papel
        with open(file_path, 'r') as file:
            ids = file.read().splitlines()

        # Verifica se o ID está na lista
        if id in ids:
            ids.remove(id)  # Remove o ID da lista original

            # Reescreve o arquivo original sem o ID removido
            with open(file_path, 'w') as file:
                file.write('\n'.join(ids))

            # Adiciona o ID ao arquivo de IDs utilizados
            with open(used_ids_path, 'a') as used_file:
                used_file.write(id + '\n')
            return True
        else:
            return False

    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro ao tentar modificar {file_path}: {e}")
        return False
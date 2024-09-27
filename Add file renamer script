import os
from datetime import datetime
from google.colab import files

# Função para fazer o upload de múltiplos arquivos no Colab
def upload_files():
    uploaded = files.upload()  # O usuário faz o upload dos arquivos
    file_paths = list(uploaded.keys())  # Retorna os nomes reais dos arquivos após o upload
    print(f"Arquivos enviados: {file_paths}")  # Imprimir lista de arquivos enviados
    return file_paths

# Função para perguntar o tipo de documento
def get_document_type():
    while True:
        print("Escolha o tipo de documento:")
        print("1. IT")
        print("2. POL")
        print("3. Mapeamento AI IS")
        print("4. Mapeamento TO")
        print("5. PO")
        
        option = input("Digite o número correspondente: ")
        document_types = {
            '1': 'IT',
            '2': 'POL',
            '3': 'Mapeamento_AI_IS',
            '4': 'Mapeamento_TO',
            '5': 'PO'
        }
        
        if option in document_types:
            return document_types[option]
        else:
            print("Opção inválida. Por favor, escolha novamente.")

# Função para perguntar o nome do documento
def get_document_name():
    document_name = input("Digite o nome do documento: ")
    return document_name

# Função para perguntar o número inicial do documento
def get_document_number_start():
    document_number_start = int(input("Digite o número inicial do documento: "))
    return document_number_start

# Função para perguntar a versão inicial
def get_version_start():
    version_start = int(input("Digite a versão inicial do documento: "))
    return version_start

# Função para perguntar a data de emissão
def get_issue_date():
    option = input("Deseja usar a data atual para a emissão? (S/N): ").lower()
    if option == 's':
        return datetime.now().strftime('%d-%m-%Y')  # Data atual no formato brasileiro (dd-mm-aaaa)
    else:
        return input("Digite a data de emissão (formato: DD-MM-AAAA): ")

# Função principal para renomear os arquivos
def rename_files(file_paths):
    if not file_paths:
        print("Nenhum arquivo foi selecionado.")
        return
    
    # Perguntar o tipo de documento
    document_type = get_document_type()
    
    # Perguntar o nome do documento
    document_name = get_document_name()
    
    # Perguntar o número inicial do documento
    document_number_start = get_document_number_start()
    
    # Perguntar a versão inicial
    version_start = get_version_start()
    
    # Perguntar a data de emissão
    issue_date = get_issue_date()
    
    renamed_files = []  # Lista para armazenar os arquivos renomeados

    # Renomear cada arquivo
    for index, file_name in enumerate(file_paths):
        # Obter a extensão do arquivo original
        _, file_extension = os.path.splitext(file_name)
        
        # Criar o novo nome do arquivo com base nas respostas e convertê-lo para maiúsculas
        document_number = document_number_start + index  # Incrementa o número do documento para cada arquivo
        version = version_start + index  # Incrementa a versão automaticamente
        new_file_name = f"{document_type}_{document_name}_{document_number}_v{version}_{issue_date}{file_extension}".upper()
        
        # Caminho completo do novo arquivo
        new_file_path = os.path.join("/content", new_file_name)
        
        # Caminho completo do arquivo carregado (usando o nome real do arquivo)
        old_file_path = os.path.join("/content", file_name)
        
        # Imprimir os caminhos completos para depuração
        print(f"Tentando renomear: {old_file_path} -> {new_file_path}")
        
        # Verificar se o arquivo existe antes de renomear
        if os.path.exists(old_file_path):
            # Renomear o arquivo localmente
            os.rename(old_file_path, new_file_path)
            print(f"Arquivo renomeado para: {new_file_name}")
            renamed_files.append(new_file_path)  # Adicionar o caminho completo à lista
        else:
            print(f"Erro: Arquivo {old_file_path} não encontrado.")
    
    return renamed_files

# Exemplo de uso
file_paths = upload_files()  # Solicitar upload de arquivos
renamed_files = rename_files(file_paths)  # Renomear os arquivos

# Faça o download dos arquivos renomeados automaticamente após o renomeio
for renamed_file in renamed_files:
    files.download(renamed_file)

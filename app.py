import os
import zipfile
from flask import Flask, request, send_file
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/content'  # Diretório para upload de arquivos

# Função para perguntar o tipo de documento com siglas atualizadas
def get_document_type():
    document_types = {
        '1': ('MG', 'Manual de Gestão'),
        '2': ('PI', 'Política Institucional/ Interna'),
        '3': ('BP', 'Book de Processos'),
        '4': ('PG', 'Procedimento da Gestão'),
        '5': ('PO', 'Procedimento Operacional'),
        '6': ('MP', 'Modelagem de Processos AS IS'),
        '7': ('IT', 'Instrução de Trabalho'),
        '8': ('DS', 'Diagrama SIPOC'),
        '9': ('RE', 'Registro'),
        '10': ('TQ', 'Tabela de Registro da Qualidade'),
        '11': ('MO', 'Manual Operacional'),
        '12': ('LM', 'Lista Mestra')
    }
    
    while True:
        print("Escolha o tipo de documento:")
        for key, value in document_types.items():
            print(f"{key}. {value[1]}")  # Exibe apenas a descrição completa
        
        option = input("Digite o número correspondente: ")
        
        if option in document_types:
            sigla, descricao = document_types[option]
            print(f"Você escolheu: {descricao}")
            return sigla  # Retorna a sigla para ser usada no nome do arquivo
        else:
            print("Opção inválida. Por favor, escolha novamente.")

# Função para renomear os arquivos
def rename_file(file_path, document_type, document_name, document_number, version, issue_date):
    # Obter a extensão do arquivo original
    _, file_extension = os.path.splitext(file_path)
    
    # Criar o novo nome do arquivo com base nas respostas
    new_file_name = f"{document_type}_{document_name}_{document_number}_v{version}_{issue_date}{file_extension}"
    
    # Caminho completo do novo arquivo
    new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_file_name)
    
    # Renomear o arquivo
    os.rename(file_path, new_file_path)
    
    return new_file_name, new_file_path

@app.route('/upload', methods=['POST'])
def upload_and_rename():
    # Receber arquivos enviados
    uploaded_files = request.files.getlist("file")
    
    # Obter os parâmetros de renomeação
    document_type = get_document_type()
    document_name = request.form.get('document_name')
    document_number_start = int(request.form.get('document_number_start'))
    version_start = int(request.form.get('version_start'))
    issue_date = request.form.get('issue_date')
    
    renamed_files = []
    
    # Renomear cada arquivo
    for index, file in enumerate(uploaded_files):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)  # Salvar o arquivo carregado no servidor
        
        # Criar o número do documento e a versão
        document_number = document_number_start + index
        version = version_start + index
        
        # Renomear o arquivo
        new_file_name, new_file_path = rename_file(file_path, document_type, document_name, document_number, version, issue_date)
        renamed_files.append(new_file_path)

    # Zipar os arquivos renomeados para download
    zip_filename = "arquivos_renomeados.zip"
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in renamed_files:
            zipf.write(file, os.path.basename(file))

    # Retornar o arquivo zipado para download
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

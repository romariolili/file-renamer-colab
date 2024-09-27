from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Definir um diretório para salvar os uploads
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota para testar se o serviço está rodando
@app.route('/')
def home():
    return "File Renamer Service is running!"

# Função para renomear arquivos
def rename_file(old_file_path, document_type, document_name, document_number, version, issue_date):
    # Obter a extensão do arquivo
    _, file_extension = os.path.splitext(old_file_path)
    
    # Criar o novo nome do arquivo com base nas informações fornecidas
    new_file_name = f"{document_type}_{document_name}_{document_number}_v{version}_{issue_date}{file_extension}".upper()
    
    # Caminho completo para o novo arquivo
    new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_file_name)
    
    # Renomear o arquivo
    os.rename(old_file_path, new_file_path)
    
    return new_file_name

# Endpoint para upload e renomear arquivos
@app.route('/upload', methods=['POST'])
def upload_and_rename():
    # Verificar se a requisição contém arquivos
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400
    
    file = request.files['file']
    
    # Verificar se o arquivo tem um nome
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400
    
    # Salvar o arquivo no diretório de uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Obter dados do formulário
    document_type = request.form.get('document_type')
    document_name = request.form.get('document_name')
    document_number = request.form.get('document_number')
    version = request.form.get('version')
    issue_date = request.form.get('issue_date')
    
    # Verificar se todos os parâmetros foram fornecidos
    if not all([document_type, document_name, document_number, version, issue_date]):
        return jsonify({'error': 'Faltam parâmetros para renomear o arquivo.'}), 400

    # Renomear o arquivo
    new_file_name = rename_file(file_path, document_type, document_name, document_number, version, issue_date)

    # Retornar o arquivo renomeado para download
    return jsonify({
        'message': 'Arquivo renomeado com sucesso!',
        'file_url': f'/download/{new_file_name}'
    })

# Endpoint para baixar o arquivo renomeado
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

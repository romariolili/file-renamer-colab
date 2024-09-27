from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from datetime import datetime

app = Flask(__name__)

# Definir um diretório para salvar os uploads
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Página inicial com formulário de upload
@app.route('/')
def home():
    return render_template('upload.html')

# Função para renomear arquivos
def rename_file(old_file_path, document_type, document_name, document_number, version, issue_date):
    _, file_extension = os.path.splitext(old_file_path)
    new_file_name = f"{document_type}_{document_name}_{document_number}_v{version}_{issue_date}{file_extension}".upper()
    new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_file_name)
    os.rename(old_file_path, new_file_path)
    return new_file_name

# Endpoint para upload e renomear arquivos
@app.route('/upload', methods=['POST'])
def upload_and_rename():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400
    
    # Lista de arquivos enviados
    files = request.files.getlist('file')

    # Obter dados do formulário
    document_type = request.form.get('document_type')
    document_name = request.form.get('document_name')
    document_number = int(request.form.get('document_number'))
    version = int(request.form.get('version'))
    issue_date = request.form.get('issue_date')
    
    # Validar se todos os parâmetros foram fornecidos
    if not all([document_type, document_name, document_number, version, issue_date]):
        return jsonify({'error': 'Faltam parâmetros para renomear o arquivo.'}), 400

    renamed_files = []

    # Salvar e renomear cada arquivo
    for file in files:
        if file.filename == '':
            continue

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Renomear o arquivo e incrementar o número do documento
        new_file_name = rename_file(file_path, document_type, document_name, document_number, version, issue_date)
        renamed_files.append(new_file_name)
        document_number += 1  # Incrementa o número do documento para o próximo arquivo

    # Retornar os arquivos renomeados
    return jsonify({
        'message': 'Arquivos renomeados com sucesso!',
        'files': renamed_files
    })

# Endpoint para baixar o arquivo renomeado
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



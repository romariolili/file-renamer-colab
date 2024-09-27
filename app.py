from flask import Flask, request, send_file, render_template, jsonify
import os
from datetime import datetime
import zipfile

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
    return new_file_name, new_file_path

# Endpoint para upload e renomear arquivos
@app.route('/upload', methods=['POST'])
def upload_and_rename():
    renamed_files = []

    # Processar cada arquivo enviado e seus respectivos parâmetros
    for i in range(len(request.files)):
        file = request.files[f'file{i}']

        # Obter parâmetros para cada arquivo
        document_type = request.form.get(f'document_type{i}')
        document_name = request.form.get(f'document_name{i}')
        document_number = request.form.get(f'document_number{i}')
        version = request.form.get(f'version{i}')
        issue_date = request.form.get(f'issue_date{i}')

        if file and document_type and document_name and document_number and version and issue_date:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

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


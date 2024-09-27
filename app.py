from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Rota para testar se o serviço está rodando
@app.route('/')
def home():
    return "File Renamer Service is running!"

# Função para renomear arquivos
def rename_file(old_file_name, document_type, document_name, document_number, version, issue_date):
    # Obter a extensão do arquivo
    _, file_extension = os.path.splitext(old_file_name)
    
    # Criar o novo nome do arquivo com base nas informações fornecidas
    new_file_name = f"{document_type}_{document_name}_{document_number}_v{version}_{issue_date}{file_extension}".upper()
    
    # Caminho completo para o novo arquivo
    new_file_path = os.path.join("/content", new_file_name)
    
    # Verificar se o arquivo existe e renomeá-lo
    if os.path.exists(old_file_name):
        os.rename(old_file_name, new_file_path)
        return new_file_name
    else:
        return None

# Endpoint para renomear arquivos
@app.route('/rename', methods=['POST'])
def rename():
    data = request.json  # Receber dados no formato JSON
    
    old_file_name = data.get('old_file_name')
    document_type = data.get('document_type')
    document_name = data.get('document_name')
    document_number = data.get('document_number')
    version = data.get('version')
    issue_date = data.get('issue_date')
    
    # Validar se todos os parâmetros foram fornecidos
    if not all([old_file_name, document_type, document_name, document_number, version, issue_date]):
        return jsonify({'error': 'Faltam parâmetros para renomear o arquivo.'}), 400

    # Renomear o arquivo
    new_file_name = rename_file(old_file_name, document_type, document_name, document_number, version, issue_date)
    
    if new_file_name:
        return jsonify({'message': f'Arquivo renomeado para {new_file_name}.'})
    else:
        return jsonify({'error': 'Arquivo não encontrado.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


import hashlib
import requests
import yaml

# Carregar configuração do arquivo YML
with open("config/config_hash.yml", 'r') as file:
    config = yaml.safe_load(file)

# URL do endpoint alvo
url = config['endpoint']

# Função para gerar hash MD5
def generate_md5_hash(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()

# Função para enviar solicitações ao servidor
def send_request(data):
    response = requests.post(url, data={'data': data})
    return response

# Lista de dados para testar colisões
data_list = config['data_list']

for data in data_list:
    hash_value = generate_md5_hash(data)
    response = send_request(data)
    print(f"Data: {data}, Hash: {hash_value}, Response: {response.text}")

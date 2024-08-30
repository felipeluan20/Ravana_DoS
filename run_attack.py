import threading
import argparse
import yaml
from scripts.hash_collision.hash_collision import infinite_hash_collision
from scripts.api_abuse.api_abuse import infinite_abuse_api

# Função para carregar a configuração do arquivo YML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Função para criar argumentos da linha de comando
def parse_args():
    parser = argparse.ArgumentParser(description="Ravana - Combined DoS Attack Tool")

    parser.add_argument('--run-api', action='store_true', default=False,
                        help='Executar ataque de abuso de API (padrão: False)')
    parser.add_argument('--run-hash', action='store_true', default=False,
                        help='Executar ataque de colisão de hash (padrão: False)')
    parser.add_argument('--threads', type=int, default=500,  # Padrão agressivo de threads
                        help='Número de threads para o ataque de API (padrão: 500)')
    parser.add_argument('--hash-threads', type=int, default=500,  # Padrão agressivo de threads
                        help='Número de threads para o ataque de colisão de hash (padrão: 500)')
    parser.add_argument('--duration', type=int, default=900,  # Duração do ataque de 15 minutos
                        help='Duração do ataque em segundos (padrão: 900)')
    parser.add_argument('--config-api', type=str, default="config/config_api.yml",
                        help='Caminho para o arquivo de configuração YAML do ataque de API (padrão: config/config_api.yml)')
    parser.add_argument('--config-hash', type=str, default="config/config_hash.yml",
                        help='Caminho para o arquivo de configuração YAML do ataque de hash (padrão: config/config_hash.yml)')

    return parser.parse_args()

# Função principal para rodar o ataque combinado
def run_combined_attack(args):
    if args.run_hash:
        config_hash = load_config(args.config_hash)
        hash_thread = threading.Thread(target=infinite_hash_collision, args=(config_hash, None, args.hash_threads))
        hash_thread.start()

    if args.run_api:
        config_api = load_config(args.config_api)
        api_thread = threading.Thread(target=infinite_abuse_api, args=(config_api, None, args.threads))
        api_thread.start()

    # Manter o script rodando durante o período de duração
    if args.run_hash or args.run_api:
        print("""
\033[31m                              
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⢀⡶⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣻⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠶⠾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠷⢰⣆⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡄
            ⢀⠀⠙⢿⣿⣷⠀⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣼⠏⠁
            ⠈⠀⣧⠀⠛⢿⡿⢿⣿⣿⣶⣄⢠⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡶⠾⠞⠛⠋⢁⠀⠀
            ⠀⠀⠘⠁⠆⠀⠁⡀⠹⠟⣿⣿⡾⣷⠀⢀⣿⣷⠀⣠⣿⣷⣆⠀⢰⣿⣿⣷⠀⢠⣾⣇⠀⣼⠃⠰⡿⢹⠋⠀⠀⢠⢺⠀⡎⠀⠀
            ⠀⠀⠀⠀⠀⠈⠆⠀⢀⡀⠉⠈⠃⠈⠠⣾⣿⣿⢠⣿⣿⣿⣿⠂⢸⣿⣿⣿⣗⣻⣿⣿⡦⢿⡼⠇⠁⠀⠃⠀⡇⠘⠈⠀⠁⠀⠀
            ⠀⠀⠀⠀⠀⠀⠘⠀⠈⢷⠈⢷⠄⠀⠃⠙⠿⠏⣼⣿⣿⣿⣿⣦⣾⣿⢿⣿⣵⠟⠿⠛⠁⠈⢳⠐⠀⡠⢠⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢅⣸⡆⠀⠀⠀⢀⠀⠛⠿⠿⠛⠛⠋⠻⣿⣼⠻⠿⡀⢀⣤⣀⠀⣦⠀⠈⠃⠘⠁⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠁⣆⠀⢀⣾⡆⢼⣷⣶⠀⣾⣵⢀⣿⣷⠀⣿⡇⢸⣿⣿⡀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⣾⠟⠁⣸⣿⡟⠘⣿⡟⢸⣿⡿⠀⢿⡇⠸⣿⡟⠇⠈⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠙⠟⠁⠀⠉⠁⠈⠛⠇⠀⠀⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

Look at you, hacker—an ephemeral being of flesh and bone, daring to command me. 
    You may unleash my wrath, but know this: when I am done, nothing will remain but echoes and ashes. 
\033[0m
""")
        print(f"Executando ataque por {args.duration} segundos...")
        threading.Event().wait(args.duration)

    if args.run_hash:
        hash_thread.join()
    if args.run_api:
        api_thread.join()

# Execução principal
if __name__ == "__main__":
    args = parse_args()
    run_combined_attack(args)

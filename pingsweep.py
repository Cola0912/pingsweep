
# 使い方　
# 特定の範囲を指定してスキャンする場合： python3 pingsweep.py 192.168.1.0/24
# 自動でローカルIP範囲を検出してスキャンする場合： python3 pingsweep.py

# 自端末のIPアドレスは青
# 新規で増えたIPアドレスは緑
# 前回の結果を参照し、接続が切れたIPアドレスは赤
# それ以外は白

import subprocess
import ipaddress
import sys
from pythonping import ping
from tqdm import tqdm
from termcolor import colored
import os
import json
import socket  # ホスト名を取得するため

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return None

def get_local_ip_range():
    ip_cmd = subprocess.check_output("ip a | grep 'inet ' | grep -v '127.0.0.1'", shell=True).decode()
    for line in ip_cmd.splitlines():
        ip_info = line.split()
        ip_addr = ip_info[1]
        if '/' in ip_addr:
            return ip_addr
    return None

def load_previous_results(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return set(json.load(file))
    return set()

def save_current_results(filename, alive_hosts):
    with open(filename, 'w') as file:
        json.dump(list(alive_hosts), file)

# 自端末のIPアドレスを取得
local_ip = get_local_ip_range()
local_ip = local_ip.split('/')[0] if local_ip else None

if len(sys.argv) > 1:
    ip_range = sys.argv[1]
else:
    ip_range = get_local_ip_range()

results_file = f"scan_results_{ip_range.replace('/', '-')}.json"

if ip_range:
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
        alive_hosts = set()
        previous_hosts = load_previous_results(results_file)

        pbar = tqdm(total=network.num_addresses - 2, desc="Scanning", unit="host")
        for ip in network.hosts():
            pbar.set_description(f"Scanning {ip}")
            pbar.refresh()

            response = ping(str(ip), count=1, timeout=1)
            if response.success():
                alive_hosts.add(str(ip))
            pbar.update(1)
        
        pbar.close()

        new_hosts = alive_hosts - previous_hosts
        gone_hosts = previous_hosts - alive_hosts

        print("\nAlive hosts:")
        for host in alive_hosts:
            hostname = get_hostname(host)
            display_text = f"{host} ({hostname})" if hostname else host
            color = None
            if host == local_ip:
                color = 'blue'
            elif host in new_hosts:
                color = 'green'
            elif host in gone_hosts:
                color = 'red'
            print(colored(display_text, color) if color else display_text)

        save_current_results(results_file, alive_hosts)
    except ValueError as e:
        print(f"Error: {e}")
else:
    print("No valid IP range provided or detected.")
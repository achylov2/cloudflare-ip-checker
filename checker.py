import socket
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
from tqdm import tqdm

init(autoreset=True)

# 📦 функция для работы внутри .exe
def get_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

INPUT_FILE = get_path("cloudflare_ipv4.txt")
OUTPUT_FILE = "working.txt"
FAILED_FILE = "failed.txt"

TIMEOUT = 1
THREADS = 300

def check_ip(ip):
    start = time.time()
    try:
        sock = socket.create_connection((ip, 443), timeout=TIMEOUT)
        latency = (time.time() - start) * 1000
        sock.close()
        return ("OK", ip, round(latency, 2))
    except:
        return ("FAIL", ip, None)

def main():
    with open(INPUT_FILE, "r") as f:
        ips = [line.strip() for line in f]

    working = []
    failed = []

    print(Fore.CYAN + f"\n🚀 Всего IP: {len(ips)}")
    print(Fore.YELLOW + "⚡ Запуск сканирования...\n")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(check_ip, ip) for ip in ips]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Проверка", ncols=100):
            status, ip, latency = future.result()

            if status == "OK":
                working.append((ip, latency))
                tqdm.write(Fore.GREEN + f"✅ {ip} → {latency} ms")
            else:
                failed.append(ip)
                tqdm.write(Fore.RED + f"❌ {ip} FAIL")

    working.sort(key=lambda x: x[1])

    with open(OUTPUT_FILE, "w") as f:
        for ip, latency in working:
            f.write(f"{ip} {latency}ms\n")

    with open(FAILED_FILE, "w") as f:
        for ip in failed:
            f.write(ip + "\n")

    print(Fore.CYAN + "\n🎯 Готово!")
    print(Fore.GREEN + f"✔ Рабочих IP: {len(working)}")
    print(Fore.RED + f"✖ Не работает: {len(failed)}")
    print(Fore.YELLOW + "📁 Файлы: working.txt / failed.txt")

if __name__ == "__main__":
    main()
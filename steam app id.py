import socket
import socks
import requests
from concurrent.futures import ThreadPoolExecutor

# Загрузка списка прокси из файла
with open("proxies.txt", "r") as f:
    proxies = [line.strip() for line in f if line.strip()]

# Проверка одного прокси
def check_proxy(proxy):
    try:
        ip, port = proxy.replace("socks4://", "").split(":")
        socks.set_default_proxy(socks.SOCKS4, ip, int(port))
        socket.socket = socks.socksocket

        response = requests.get("http://ipinfo.io/ip", timeout=5)
        print(f"[✅] Работает: {proxy} → {response.text.strip()}")
        return proxy
    except Exception as e:
        print(f"[❌] Не работает: {proxy}")
        return None

# Многопоточная проверка
with ThreadPoolExecutor(max_workers=30) as executor:
    working = list(filter(None, executor.map(check_proxy, proxies)))

# Сохранение рабочих прокси
with open("working_socks4.txt", "w") as f:
    for proxy in working:
        f.write(proxy + "\n")
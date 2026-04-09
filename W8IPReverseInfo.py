import socket
import requests
import os
import time
import threading
import ipaddress
import asyncio
from urllib.parse import urlparse
from colorama import Fore, init

init(autoreset=True)

lock = threading.Lock()

# =========================
# 🔹 CONFIG
# =========================
MAX_CONCURRENT = 800
OUTPUT_FILE = "deep_scan.txt"

# =========================
# 🔹 CLEAR SCREEN
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# =========================
# 🔹 LOADING
# =========================
def loading():
    for i in range(3):
        print(Fore.GREEN + "[+] Initializing Tool" + "." * (i+1))
        time.sleep(0.3)
        clear()

# =========================
# 🔹 BANNER
# =========================
def banner():
    print(Fore.RED + r"""
██╗    ██╗ █████╗ ██████╗ ██████╗ 
██║    ██║██╔══██╗╚══██╔══╝██╔══██╗
██║ █╗ ██║╚█████╔╝   ██║   ██████╔╝
██║███╗██║██╔══██╗   ██║   ██╔═══╝ 
╚███╔███╔╝╚█████╔╝ ██████╗ ██║     
 ╚══╝╚══╝  ╚════╝  ╚═════╝ ╚═╝     

        W8IP PRO MAX SCANNER
""")
    print(Fore.GREEN + "   Coded by W8Team / MD SOJIB\n")

# =========================
# 🔹 DOMAIN CLEAN
# =========================
def clean_domain(input_value):
    if input_value.startswith("http"):
        return urlparse(input_value).netloc
    return input_value.strip()

# =========================
# 🔹 DOMAIN LOOKUP
# =========================
def lookup(target):
    print(Fore.YELLOW + "\n[🔍] Processing...\n")

    domain = clean_domain(target)

    try:
        ip = socket.gethostbyname(domain)
    except:
        print(Fore.RED + "[!] Invalid domain\n")
        return

    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        hostname = "Not Found"

    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=5).json()
    except:
        res = {}

    print(Fore.GREEN + "="*50)
    print(Fore.GREEN + f"🌐 Domain     : {domain}")
    print(Fore.GREEN + f"🟢 IP         : {ip}")
    print(Fore.CYAN + f"🧠 Hostname   : {hostname}")
    print(Fore.GREEN + "-"*50)
    print(Fore.YELLOW + f"🌍 Country    : {res.get('country','Unknown')}")
    print(Fore.YELLOW + f"🏙️ City       : {res.get('city','Unknown')}")
    print(Fore.YELLOW + f"📡 ISP        : {res.get('isp','Unknown')}")
    print(Fore.YELLOW + f"🏢 Org        : {res.get('org','Unknown')}")
    print(Fore.YELLOW + f"🔢 ASN        : {res.get('as','Unknown')}")
    print(Fore.GREEN + "="*50 + "\n")

# =========================
# 🔹 EXTRACT TITLE
# =========================
def extract_title(html):
    try:
        html = html.lower()
        if "<title>" in html:
            return html.split("<title>")[1].split("</title>")[0].strip()
    except:
        pass
    return None

# =========================
# 🔹 IP SCAN (OPTION 2)
# =========================
def scan_ip(ip):
    ip = str(ip)

    hostname = None
    server = None
    title = None

    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        pass

    try:
        r = requests.get(f"http://{ip}", timeout=2)
        server = r.headers.get("Server")
        title = extract_title(r.text)
    except:
        pass

    if not hostname and not server:
        return

    with lock:
        print(Fore.GREEN + f"[+] {ip}")
        if hostname:
            print(Fore.CYAN + f"    Hostname : {hostname}")
        if server:
            print(Fore.YELLOW + f"    Server   : {server}")
        if title:
            print(Fore.BLUE + f"    Title    : {title}")
        print("-"*40)

# =========================
# 🔹 CIDR SCAN
# =========================
def cidr_scan(cidr):
    print(Fore.YELLOW + f"\n[⚡] Scanning: {cidr}\n")

    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except:
        print("Invalid CIDR")
        return

    threads = []

    for ip in network.hosts():
        t = threading.Thread(target=scan_ip, args=(ip,))
        t.start()
        threads.append(t)

        if len(threads) >= 100:
            for th in threads:
                th.join()
            threads = []

    for th in threads:
        th.join()

    print(Fore.CYAN + "\n[✔] Scan Completed\n")

# =========================
# 🔹 SAVE RESULT
# =========================
def save_line(text):
    with open(OUTPUT_FILE, "a") as f:
        f.write(text + "\n")

# =========================
# 🔹 ASYNC PORT CHECK
# =========================
async def check_port(ip, port, sem):
    async with sem:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=0.5
            )

            print(Fore.GREEN + f"   [OPEN] {port}")
            save_line(f"{ip}:{port}")

            writer.close()
            await writer.wait_closed()
        except:
            pass

# =========================
# 🔹 DEEP SCAN IP
# =========================
async def deep_scan_ip(ip):
    print(Fore.CYAN + f"\n[🔍] Scanning IP: {ip}")

    # hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        print(Fore.YELLOW + f"   Hostname : {hostname}")
        save_line(f"{ip} Hostname: {hostname}")
    except:
        pass

    # server + title
    try:
        r = requests.get(f"http://{ip}", timeout=2)
        server = r.headers.get("Server")
        title = extract_title(r.text)

        if server:
            print(Fore.YELLOW + f"   Server   : {server}")
            save_line(f"{ip} Server: {server}")

        if title:
            print(Fore.YELLOW + f"   Title    : {title}")
            save_line(f"{ip} Title: {title}")
    except:
        pass

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    tasks = [
        check_port(ip, port, sem)
        for port in range(1, 65536)
    ]

    await asyncio.gather(*tasks)

# =========================
# 🔹 DEEP SCAN NETWORK
# =========================
async def deep_scan_network(cidr):
    print(Fore.RED + f"\n[🔥] FULL DEEP SCAN: {cidr}\n")

    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except:
        print("Invalid CIDR")
        return

    open(OUTPUT_FILE, "w").close()

    try:
        for ip in network.hosts():
            await deep_scan_ip(str(ip))
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Stopped by CTRL+C\n")
        return

    print(Fore.GREEN + f"\n[✔] Saved → {OUTPUT_FILE}\n")

# =========================
# 🔹 MAIN MENU
# =========================
def main():
    loading()
    clear()
    banner()

    while True:
        print("""
[1] Domain → IP + Info
[2] IP Range Scan (/24 + Server + Title)
[3] Deep Scan (ALL PORTS ⚡ + Server + Title + Save)
[4] Exit
""")

        choice = input("Select ➤ ")

        if choice == "1":
            target = input("Domain ➤ ")
            lookup(target)

        elif choice == "2":
            cidr = input("CIDR ➤ ")
            cidr_scan(cidr)

        elif choice == "3":
            cidr = input("CIDR ➤ ")
            asyncio.run(deep_scan_network(cidr))

        elif choice == "4":
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()

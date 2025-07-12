import requests
import threading
import sys
import time
from datetime import datetime

# Validate and accept domain from command line
if len(sys.argv) != 2:
    print("Usage: python subdomain_enum.py <target-domain>")
    sys.exit(1)

domain = sys.argv[1].strip()
if not domain:
    print("[!] Invalid domain name.")
    sys.exit(1)

# Start timestamp
start_time = datetime.now()
print(f"\n[~] Subdomain Enumeration Started for: {domain}")
print(f"[~] Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# List to store discovered subdomains
discovered_subdomains = []

# Lock for thread-safe list access
lock = threading.Lock()

# Load subdomain wordlist from file
try:
    with open("subdomains.txt", "r") as file:
        subdomains = file.read().splitlines()
except FileNotFoundError:
    print("[!] subdomains.txt not found. Please create it with a list of subdomain prefixes.")
    sys.exit(1)

# Function to check if subdomain exists
def check_subdomain(subdomain):
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code < 400:
            with lock:
                print(f"[+] Found: {url}")
                discovered_subdomains.append(url)
    except (requests.ConnectionError, requests.Timeout):
        pass

# Create and start threads
threads = []
for sub in subdomains:
    t = threading.Thread(target=check_subdomain, args=(sub,))
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()

# Save discovered subdomains to file
output_file = "discovered_subdomains.txt"
with open(output_file, "w") as file:
    for url in discovered_subdomains:
        file.write(url + "\n")

# Completion timestamp
end_time = datetime.now()
duration = end_time - start_time

print(f"\n[✓] Enumeration complete. {len(discovered_subdomains)} subdomains found.")
print(f"[✓] Results saved to {output_file}")
print(f"[✓] Duration: {duration.total_seconds():.2f} seconds\n")


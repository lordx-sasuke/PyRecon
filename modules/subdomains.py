import requests

def enumerate_subdomains(domain):
    print(f"\n[*] Querying HackerTarget API for subdomains of: {domain}...")
    subdomains = []
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            lines = res.text.strip().split('\n')
            if "error" in lines[0].lower() or "no records" in lines[0].lower():
                print(" [-] No records found or API limit reached.")
                return subdomains

            for line in lines:
                parts = line.split(',')
                if len(parts) >= 2:
                    subdomains.append({'subdomain': parts[0], 'ip': parts[1]})
                    print(f"  [+] {parts[0]} - {parts[1]}")
    except Exception as e:
        print(f" [!] Network Error: {e}")
    return subdomains

import requests

def analyze_headers(url):
    print(f"\n[*] Analyzing HTTP Security Headers for: {url}")
    # Common security headers to check for
    security_headers = [
        'Strict-Transport-Security',
        'Content-Security-Policy',
        'X-Frame-Options',
        'X-Content-Type-Options',
        'Referrer-Policy'
    ]
    
    try:
        # We spoof a standard browser to prevent WAF blocks
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0.0.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        server_header = response.headers.get('Server', 'Unknown')
        print(f" [+] Server Software: {server_header}")
        
        print("\n [*] Header Security Status:")
        for header in security_headers:
            if header in response.headers:
                print(f"  [+] {header}: Enabled")
            else:
                print(f"  [-] {header}: Missing")
                
    except requests.exceptions.RequestException as e:
        print(f" [!] Failed to connect: {e}")

def get_robots_txt(url):
    print("\n[*] Fetching robots.txt to find hidden paths...")
    # Normalize URL to ensure it ends cleanly
    base_url = url.rstrip('/')
    robots_url = f"{base_url}/robots.txt"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0.0.0'}
        response = requests.get(robots_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            lines = response.text.splitlines()
            disallowed = [line for line in lines if line.strip().startswith('Disallow:')]
            
            if disallowed:
                print(f" [+] Found {len(disallowed)} restricted paths. Top 5:")
                for path in disallowed[:5]:
                    print(f"     {path}")
            else:
                print(" [+] robots.txt found, but no Disallow rules specified.")
        else:
            print(" [-] No robots.txt found on this server.")
            
    except requests.exceptions.RequestException as e:
        print(f" [!] Failed to retrieve robots.txt: {e}")

# Simple test block so you can run this module by itself
if __name__ == "__main__":
    target = "https://hackerone.com"
    analyze_headers(target)
    get_robots_txt(target)

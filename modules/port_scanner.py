import socket

def scan_ports(ip_or_domain, ports):
    print(f"\n[*] Starting Targeted Port Scan on: {ip_or_domain}")
    open_ports = []
    
    # Resolve domain to IP if a hostname is provided
    try:
        target_ip = socket.gethostbyname(ip_or_domain)
        if target_ip != ip_or_domain:
            print(f" [*] Resolved to IP: {target_ip}")
    except socket.gaierror:
        print(" [!] Could not resolve host.")
        return open_ports

    for port in ports:
        try:
            # AF_INET for IPv4, SOCK_STREAM for TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0) # 1-second timeout to maintain speed
            
            # connect_ex returns 0 if the connection is successful
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                print(f" [+] Port {port}/TCP: OPEN")
                open_ports.append(port)
            sock.close()
        except Exception:
            pass # Silently ignore errors to keep output clean
            
    if not open_ports:
        print(" [-] No open ports found in the specified range.")
        
    return open_ports

if __name__ == "__main__":
    # Test block using safe default
    target = "example.com"
    common_ports = [21, 22, 23, 80, 443, 3306, 8080, 8443]
    scan_ports(target, common_ports)

import ssl
import socket
import datetime

def inspect_certificate(domain, port=443):
    print(f"\n[*] Inspecting SSL/TLS Certificate for: {domain}:{port}")
    
    # Create a default secure context
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((domain, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Extract Issuer and Subject data safely
                issuer = dict(x[0] for x in cert.get('issuer', []))
                subject = dict(x[0] for x in cert.get('subject', []))
                
                print(f" [+] Issued To: {subject.get('commonName', 'Unknown')}")
                print(f" [+] Issued By: {issuer.get('organizationName', 'Unknown')}")
                
                # Format expiration dates
                valid_from = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                valid_to = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                
                print(f" [+] Valid From: {valid_from}")
                print(f" [+] Valid To: {valid_to}")
                
                # Extract Subject Alternative Names (SANs) - Goldmine for subdomains
                if 'subjectAltName' in cert:
                    print(" [+] Subject Alternative Names (SANs):")
                    for san in cert['subjectAltName']:
                        # san is a tuple like ('DNS', 'www.example.com')
                        print(f"     - {san[1]}")
                        
    except socket.gaierror:
        print(" [!] Could not resolve host for SSL inspection.")
    except socket.timeout:
        print(" [!] Connection timed out.")
    except ssl.SSLError as e:
        print(f" [!] SSL Negotiation Failed: {e}")
    except Exception as e:
        print(f" [!] Error: {e}")

if __name__ == "__main__":
    # Test block using safe default
    inspect_certificate("example.com")

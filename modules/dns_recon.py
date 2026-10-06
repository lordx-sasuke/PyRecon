import dns.resolver

def enumerate_dns(domain):
    print(f"\n[*] Enumerating DNS Records for: {domain}")
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']

    # configure=False stops it from looking for /etc/resolv.conf
    resolver = dns.resolver.Resolver(configure=False)
    # Explicitly route our lookups through Cloudflare and Google DNS
    resolver.nameservers = ['1.1.1.1', '8.8.8.8']

    resolver.timeout = 5
    resolver.lifetime = 5

    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            print(f"\n [+] {rtype} Records:")
            for rdata in answers:
                print(f"     {rdata.to_text()}")
        except dns.resolver.NoAnswer:
            print(f"\n [-] No {rtype} Records found.")
        except dns.resolver.NXDOMAIN:
            print(f"\n [!] Domain does not exist.")
            break
        except Exception as e:
            print(f"\n [!] Error retrieving {rtype} Records: {e}")

if __name__ == "__main__":
    # Test block for standalone execution
    target = "hackerone.com"
    enumerate_dns(target)


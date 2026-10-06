import argparse
import os
import sys

# Add parent directory to path for clean package imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.subdomains import enumerate_subdomains
from modules.web_analysis import analyze_headers, get_robots_txt
from modules.dns_recon import enumerate_dns
from modules.port_scanner import scan_ports
from modules.ssl_recon import inspect_certificate
from reports.exporter import generate_html_report

def main():
    parser = argparse.ArgumentParser(description="PyRecon - Modular OSINT & Reconnaissance Framework")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("--all", action="store_true", help="Execute complete reconnaissance suite")
    parser.add_argument("-o", "--output", help="Path to write HTML report (e.g. report.html)")
    
    args = parser.parse_args()
    domain = args.domain
    results = {}

    print(f"==================================================")
    print(f" PyRecon: Reconnaissance Initialized on {domain}")
    print(f"==================================================")

    if args.all:
        results['subdomains'] = enumerate_subdomains(domain)
        analyze_headers(f"https://{domain}")
        get_robots_txt(f"https://{domain}")
        enumerate_dns(domain)
        inspect_certificate(domain)
        results['ports'] = scan_ports(domain, [21, 22, 25, 80, 443, 8080, 8443])

    if args.output:
        generate_html_report(domain, results, args.output)

if __name__ == "__main__":
    main()

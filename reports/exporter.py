import os
import datetime

def generate_html_report(domain, data, output_path):
    report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    subdomains_rows = "".join([f"<tr><td>{item['subdomain']}</td><td>{item['ip']}</td></tr>" for item in data.get('subdomains', [])])
    ports_rows = "".join([f"<tr><td>{port}</td><td>TCP</td><td>OPEN</td></tr>" for port in data.get('ports', [])])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>PyRecon Report - {domain}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 24px; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 8px; }}
        h2 {{ color: #94a3b8; margin-top: 24px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; background: #1e293b; border-radius: 6px; overflow: hidden; }}
        th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background-color: #0284c7; color: #ffffff; }}
        .badge {{ background: #0284c7; padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>PyRecon Security Assessment: {domain}</h1>
    <p>Scan Generated: <strong>{report_time}</strong></p>
    
    <h2>Subdomains & IP Addresses ({len(data.get('subdomains', []))})</h2>
    <table>
        <tr><th>Subdomain</th><th>Resolved IP</th></tr>
        {subdomains_rows if subdomains_rows else "<tr><td colspan='2'>None identified</td></tr>"}
    </table>

    <h2>Open Ports ({len(data.get('ports', []))})</h2>
    <table>
        <tr><th>Port</th><th>Protocol</th><th>State</th></tr>
        {ports_rows if ports_rows else "<tr><td colspan='3'>No open ports detected</td></tr>"}
    </table>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n[+] HTML report saved successfully to: {output_path}")

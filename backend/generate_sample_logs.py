"""Generates a realistic sample Apache access log for testing."""
import random
from datetime import datetime, timedelta

LEGIT_IPS    = [f"192.168.1.{i}" for i in range(1, 20)]
ATTACKER_IPS = ["10.0.0.66", "185.220.101.34", "45.33.32.156", "203.0.113.5"]
SCANNER_IP   = "172.16.0.99"

LEGIT_PATHS = [
    "/", "/index.html", "/about", "/contact", "/products",
    "/api/users", "/static/style.css", "/favicon.ico", "/blog"
]
SENSITIVE_PATHS = [
    "/.env", "/.git/config", "/wp-admin", "/phpMyAdmin",
    "/backup.sql", "/config.php", "/admin", "/.htaccess"
]
SQLI_PATHS = [
    "/search?q=' OR 1=1--",
    "/login?user=admin'--",
    "/api?id=1 UNION SELECT * FROM users",
    "/items?id=1 AND sleep(5)"
]
XSS_PATHS = [
    "/search?q=<script>alert(1)</script>",
    "/comment?text=<img src=x onerror=alert(document.cookie)>",
    "/name?val=javascript:alert(1)"
]
TRAVERSAL_PATHS = [
    "/../../../etc/passwd",
    "/%2e%2e/%2e%2e/etc/shadow",
    "/files?path=../windows/system32/config"
]

LEGIT_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
]
SCANNER_AGENTS = ["Nikto/2.1.6", "sqlmap/1.7", "Nuclei/3.1", "DirBuster-1.0-RC1"]

def rand_time(base, spread_hours=48):
    offset = timedelta(seconds=random.randint(0, spread_hours * 3600))
    return (base + offset).strftime("%d/%b/%Y:%H:%M:%S +0000")

def line(ip, t, method, path, status, size, agent):
    return f'{ip} - - [{t}] "{method} {path} HTTP/1.1" {status} {size} "-" "{agent}"'

def generate(filename="sample_access.log", total=2500):
    base = datetime(2025, 6, 1)
    entries = []

    # Normal traffic
    for _ in range(int(total * 0.68)):
        ip   = random.choice(LEGIT_IPS)
        path = random.choice(LEGIT_PATHS)
        st   = random.choices([200, 304, 404], weights=[85, 10, 5])[0]
        entries.append(line(ip, rand_time(base), "GET", path, st,
                            random.randint(200, 8000), random.choice(LEGIT_AGENTS)))

    # Scanner (high volume + sensitive paths + known agent)
    for path in SENSITIVE_PATHS * 6:
        entries.append(line(SCANNER_IP, rand_time(base), "GET", path, 404, 150, "Nikto/2.1.6"))
    for _ in range(220):
        entries.append(line(SCANNER_IP, rand_time(base), "GET",
                            random.choice(LEGIT_PATHS), 200, 500, "Nikto/2.1.6"))

    # SQLi attacker
    for path in SQLI_PATHS * 4:
        entries.append(line(ATTACKER_IPS[0], rand_time(base), "GET", path, 500, 0,
                            random.choice(LEGIT_AGENTS)))

    # XSS attacker
    for path in XSS_PATHS * 4:
        entries.append(line(ATTACKER_IPS[1], rand_time(base), "GET", path, 200, 1500,
                            random.choice(LEGIT_AGENTS)))

    # Path traversal
    for path in TRAVERSAL_PATHS * 5:
        entries.append(line(ATTACKER_IPS[2], rand_time(base), "GET", path, 403, 0,
                            random.choice(LEGIT_AGENTS)))

    # Brute force (many 401s from one IP)
    for _ in range(60):
        entries.append(line(ATTACKER_IPS[3], rand_time(base), "POST", "/login", 401, 0,
                            random.choice(LEGIT_AGENTS)))

    random.shuffle(entries)
    with open(filename, 'w') as f:
        f.write('\n'.join(entries))
    print(f"Generated {len(entries):,} log lines → {filename}")

if __name__ == '__main__':
    generate()
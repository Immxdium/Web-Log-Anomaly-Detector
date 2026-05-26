import time

import requests

_cache = {}

def get_geo(ip):
    if ip in _cache:
        return _cache[ip]
    try:
        resp = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,query",
            timeout=3
        )
        if resp.status_code == 200:
            data = resp.json()
            _cache[ip] = data
            time.sleep(0.15)
            return data
    except Exception:
        pass
    return {'query': ip, 'country': 'Unknown', 'city': '-', 'isp': '-'}

def enrich_ips(ip_list):
    results = []
    local = {'127.0.0.1', 'localhost', '::1', '0.0.0.0'}
    for ip in ip_list:
        if ip in local:
            results.append({'query': ip, 'country': 'LOCAL', 'city': '-', 'isp': '-'})
        else:
            results.append(get_geo(ip))
    return results
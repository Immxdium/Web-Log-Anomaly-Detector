import re

import pandas as pd

SENSITIVE_PATHS = [
    r'\.env', r'\.git', r'wp-admin', r'phpMyAdmin',
    r'config\.php', r'\.htaccess', r'backup', r'\.sql',
    r'shell\.php', r'cmd\.php', r'/admin', r'\.bak',
    r'web\.config', r'\.DS_Store', r'passwd', r'shadow'
]

SQLI_PATTERNS = [
    r"(?i)(union[\s+]select)", r"(?i)(or\s+1\s*=\s*1)",
    r"(?i)(drop\s+table)", r"(?i)(insert\s+into)",
    r"(?i)(sleep\(\d+\))", r"(?i)(benchmark\()",
    r"'--", r"'\s+or\s+'", r"%27", r"0x[0-9a-fA-F]+"
]

XSS_PATTERNS = [
    r"(?i)<script", r"(?i)javascript:", r"(?i)onerror=",
    r"(?i)onload=", r"(?i)alert\(", r"(?i)document\.cookie",
    r"(?i)<img[^>]+src", r"(?i)eval\("
]

PATH_TRAVERSAL = [
    r"\.\./", r"\.\.\\", r"%2e%2e", r"%2E%2E",
    r"\.\.%2f", r"\.\.%5c", r"/etc/passwd", r"/proc/self",
]

SCANNER_AGENTS = [
    "nikto", "sqlmap", "nmap", "masscan", "nuclei",
    "dirbuster", "gobuster", "wfuzz", "burpsuite",
    "zgrab", "httpscan", "metasploit", "openvas",
    "hydra", "medusa", "acunetix", "nessus"
]

def _match_any(value, patterns):
    return any(re.search(p, value) for p in patterns)

def detect_all(df):
    results = {}
    
    # 1. Known scanner user-agents
    scanner_mask = df['agent'].str.lower().apply(
        lambda a: any(s in a for s in SCANNER_AGENTS)
    )
    scanner_df = df[scanner_mask].groupby('ip').agg(
        requests=('path', 'count'),
        agent=('agent', 'first')
    ).reset_index().sort_values('requests', ascending=False)
    results['scanner_agents'] = {
        'title': 'Known scanner user-agents detected',
        'severity': 'HIGH',
        'data': scanner_df,
        'count': len(scanner_df)
    }
    
    # 2. SQL injection attempts
    sqli_mask = df['path'].apply(lambda p: _match_any(p, SQLI_PATTERNS))
    sqli_df = df[sqli_mask].groupby('ip').agg(
        attempts=('path', 'count'),
        sample_path=('path', 'first')
    ).reset_index().sort_values('attempts', ascending=False)
    results['sqli']= {
        'title': 'SQL injection attempts',
        'severity': 'HIGH',
        'data': sqli_df,
        'count': int(sqli_mask.sum())
    }
    
    # 3. XSS attempts
    xss_mask = df['path'].apply(lambda p: _match_any(p, XSS_PATTERNS))
    xss_df = df[xss_mask].groupby('ip').agg(
        attempts=('path', 'count'),
        sample_path=('path', 'first')
    ).reset_index().sort_values('attempts', ascending=False)
    results['xss'] = {
        'title': 'XSS attempts',
        'severity': 'HIGH',
        'data': xss_df,
        'count': int(xss_mask.sum())
    }
    
    # 4. Path traversal attempts
    trav_mask = df['path'].apply(lambda p: _match_any(p, PATH_TRAVERSAL))
    trav_df = df[trav_mask].groupby('ip').agg(
        attempts=('path', 'count'),
        sample_path=('path', 'first')
    ).reset_index().sort_values('attempts', ascending=False)
    results['path_traversal'] = {
        'title': 'Path traversal attempts',
        'severity': 'HIGH',
        'data': trav_df,
        'count': int(trav_mask.sum())
    }
    
    # 5. Sensitive path probing
    sens_mask = df['path'].apply(lambda p: _match_any(p, SENSITIVE_PATHS))
    sens_df = df[sens_mask].groupby('ip').agg(
        probes=('path', 'count'),
        unique_paths=('path', 'nunique'),
        sample_path=('path', 'first')
    ).reset_index().sort_values('probes', ascending=False)
    results['sensitive_paths'] = {
        'title': 'Sensitive path probing',
        'severity': 'MEDIUM',
        'data': sens_df,
        'count': int(sens_mask.sum())
    }
    
    # 6. Brute force - 10+ auth failures from one IP
    auth_fail = df[df['status'].isin([401, 403])]
    brute_df = auth_fail.groupby('ip').size().reset_index(name='failures')
    brute_df = brute_df[brute_df['failures'] >= 10].sort_values('failures', ascending=False)
    results['brute_force'] = {
        'title': 'Possible brute force (10+ auth failures from one IP)',
        'severity': 'HIGH',
        'data': brute_df,
        'count': len(brute_df)
    }
    
    # 7. High request volume - 100+ requests from one IP
    vol_df = df.groupby('ip').size().reset_index(name='total_requests')
    vol_df = vol_df[vol_df['total_requests'] >= 100].sort_values('total_requests', ascending=False)
    results['high_volume'] = {
        'title': 'High request volume (100+ requests from one IP)',
        'severity': 'MEDIUM',
        'data': vol_df,
        'count': len(vol_df)
    }
    
    # 8. Error spike - 20+ errors from one IP
    err_df = df[df['status'] >= 400].groupby('ip').size().reset_index(name='errors')
    err_df = err_df[err_df['errors'] >= 20].sort_values('errors', ascending=False)
    results['error_spike'] = {
        'title': 'Error rate spike (20+ 4xx/5xx from one IP)',
        'severity': 'MEDIUM',
        'data': err_df,
        'count': len(err_df)
    }
    
    return results
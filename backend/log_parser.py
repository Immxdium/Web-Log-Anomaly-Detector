import re
from datetime import datetime

import pandas as pd

LOG_PATTERN = re.compile(r'(?P<ip>\S+)\s+'
    r'\S+\s+'
    r'\S+\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+'
    r'(?P<path>\S+)\s+'
    r'\S+"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<size>\S+)'
    r'(?:\s+"(?P<referer>[^"]*)")?'
    r'(?:\s+"(?P<agent>[^"]*)")?'
)

TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

def parse_log_line(line):
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    d = match.groupdict()
    try:
        d['time'] = datetime.strptime(d['time'], TIME_FORMAT)
    except ValueError:
        d['time'] = None
    try:
        d['status'] = int(d['status'])
    except Exception:
        d['status'] = 0
    try:
        d['size'] = int(d['size'])
    except Exception:
        d['size'] = 0
    d.setdefault('agent', '')
    d.setdefault('referer', '')
    return d


def parse_log_file(filepath):
    records = []
    with open(filepath, 'r', errors='replace') as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                records.append(parsed)
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    df['time'] = pd.to_datetime(df['time'], utc=True, errors='coerce')
    df['agent'] = df['agent'].fillna('')
    df['path'] = df['path'].fillna('')
    return df
        


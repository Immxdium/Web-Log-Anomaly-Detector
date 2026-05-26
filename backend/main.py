import argparse
import json
import sys
from pathlib import Path

from rich.console import Console

from detectors import detect_all
from log_parser import parse_log_file
from reporter import print_report

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description='Web Log Anomaly Detector — find suspicious patterns in Apache/Nginx logs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python main.py access.log
  python main.py access.log --json
  python main.py access.log --geo
  python main.py access.log --output report.json
        """
    )
    parser.add_argument('logfile',           help='Path to Apache/Nginx access log')
    parser.add_argument('--json',  action='store_true', help='Print results as JSON')
    parser.add_argument('--geo',   action='store_true', help='Enrich flagged IPs with geo data')
    parser.add_argument('--output', metavar='FILE',     help='Save JSON report to file')

    args = parser.parse_args()
    log_path = Path(args.logfile)

    if not log_path.exists():
        console.print(f"[red]Error:[/red] File not found: {args.logfile}")
        sys.exit(1)

    console.print(f"[cyan]Parsing:[/cyan] {args.logfile} ...")
    df = parse_log_file(args.logfile)

    if df.empty:
        console.print("[red]No valid log entries parsed. Check the log format.[/red]")
        sys.exit(1)

    console.print(f"[green]Loaded {len(df):,} entries[/green]")
    results = detect_all(df)

    if args.geo:
        from geo import enrich_ips
        flagged_ips = set()
        for r in results.values():
            if r['count'] > 0 and r['data'] is not None and 'ip' in r['data'].columns:
                flagged_ips.update(r['data']['ip'].tolist())
        console.print(f"[cyan]Fetching geo data for {len(flagged_ips)} IPs...[/cyan]")
        geo_list = enrich_ips(list(flagged_ips))
        geo_map  = {g.get('query', ''): g for g in geo_list}
        console.print("[green]Geo lookup complete[/green]")
        for r in results.values():
            if r['count'] > 0 and r['data'] is not None and 'ip' in r['data'].columns:
                r['data']['country'] = r['data']['ip'].map(
                    lambda ip: geo_map.get(ip, {}).get('country', '?')
                )

    if args.json or args.output:
        output = {}
        for name, r in results.items():
            output[name] = {
                'title':    r['title'],
                'severity': r['severity'],
                'count':    r['count'],
                'entries':  r['data'].to_dict(orient='records') if r['data'] is not None else []
            }
        json_str = json.dumps(output, indent=2, default=str)
        if args.output:
            Path(args.output).write_text(json_str)
            console.print(f"[green]Report saved → {args.output}[/green]")
        if args.json:
            print(json_str)
    else:
        print_report(df, results, args.logfile)

if __name__ == '__main__':
    main()
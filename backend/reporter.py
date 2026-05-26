from datetime import datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

SEVERITY_STYLE = {
    'HIGH':   ('red',    '🔴'),
    'MEDIUM': ('yellow', '🟡'),
    'LOW':    ('green',  '🟢'),
}

def print_banner(filepath):
    console.print()
    console.print(
        "[bold cyan]██╗      ██████╗  ██████╗     ██████╗ ███████╗████████╗[/bold cyan]"
    )
    console.print(
        "[bold cyan]██║     ██╔═══██╗██╔════╝     ██╔══██╗██╔════╝╚══██╔══╝[/bold cyan]"
    )
    console.print(
        "[bold cyan]██║     ██║   ██║██║  ███╗    ██║  ██║█████╗     ██║   [/bold cyan]"
    )
    console.print(
        "[bold cyan]██║     ██║   ██║██║   ██║    ██║  ██║██╔══╝     ██║   [/bold cyan]"
    )
    console.print(
        "[bold cyan]███████╗╚██████╔╝╚██████╔╝    ██████╔╝███████╗   ██║   [/bold cyan]"
    )
    console.print(
        "[bold cyan]╚══════╝ ╚═════╝  ╚═════╝     ╚═════╝ ╚══════╝   ╚═╝  [/bold cyan]"
    )
    console.print(
        f"[dim]Web Log Anomaly Detector  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  {filepath}[/dim]\n"
    )

def print_summary(df, results):
    total_reqs   = len(df)
    unique_ips   = df['ip'].nunique()
    high_count   = sum(r['count'] for r in results.values() if r['severity'] == 'HIGH')
    medium_count = sum(r['count'] for r in results.values() if r['severity'] == 'MEDIUM')

    console.print(Panel(
        f"[bold]Requests:[/bold] {total_reqs:,}     "
        f"[bold]Unique IPs:[/bold] {unique_ips}     "
        f"[red bold]HIGH alerts: {high_count}[/red bold]     "
        f"[yellow bold]MEDIUM alerts: {medium_count}[/yellow bold]",
        title="[bold white] Summary",
        border_style="cyan"
    ))

def print_detection(result):
    data     = result['data']
    severity = result['severity']
    color, icon = SEVERITY_STYLE.get(severity, ('white', '⚪'))

    if data is None or len(data) == 0:
        return

    console.print(
        f"\n[{color}]{icon}  {result['title']}[/{color}]  "
        f"[dim]({result['count']} events)[/dim]"
    )

    table = Table(
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style=f"bold {color}",
        padding=(0, 1)
    )

    for col in data.columns:
        table.add_column(col.upper())

    for _, row in data.head(10).iterrows():
        table.add_row(*[str(v)[:80] for v in row.values])

    console.print(table)

def print_report(df, results, filepath):
    print_banner(filepath)
    print_summary(df, results)

    console.print(
        "\n[bold cyan]━━━━━━━━━━━━━━━━━━━━━━ DETECTIONS ━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]"
    )

    order   = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    sorted_ = sorted(results.items(), key=lambda x: order.get(x[1]['severity'], 3))

    found = False
    for _, result in sorted_:
        if result['count'] > 0:
            print_detection(result)
            found = True

    if not found:
        console.print("\n[green]✓  No anomalies detected.[/green]")

    console.print(
        "\n[dim]Top 10 results shown per category. Use --json for full output.[/dim]\n"
    )
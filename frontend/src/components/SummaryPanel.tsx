import type { Summary } from '@/types'

interface SummaryPanelProps {
  summary: Summary
}

export function SummaryPanel({ summary }: SummaryPanelProps) {
  const metrics = [
    {
      label: 'Total Requests',
      value: summary.total_requests.toLocaleString(),
      sub:   `from ${summary.unique_ips} unique IPs`,
      color: 'text-white',
    },
    {
      label: 'High Severity',
      value: summary.high_alerts,
      sub:   'immediate action needed',
      color: 'text-red-400',
    },
    {
      label: 'Medium Severity',
      value: summary.medium_alerts,
      sub:   'monitor closely',
      color: 'text-yellow-400',
    },
    {
      label: 'Clean Traffic',
      value: `${Math.round(
        ((summary.total_requests - summary.high_alerts - summary.medium_alerts)
          / summary.total_requests) * 100
      )}%`,
      sub:   'no anomalies detected',
      color: 'text-emerald-400',
    },
  ]

  return (
    <div className="mb-6 grid grid-cols-2 gap-3 md:grid-cols-4">
      {metrics.map((m) => (
        <div
          key={m.label}
          className="liquid-glass flex flex-col gap-1.5 rounded-2xl p-5"
        >
          <div className="text-[11px] font-normal uppercase tracking-wider
                          text-white/45">
            {m.label}
          </div>
          <div
            className={`text-3xl leading-none tracking-[-1px] ${m.color}`}
            style={{ fontFamily: 'Instrument Serif, serif', fontStyle: 'italic' }}
          >
            {m.value}
          </div>
          <div className="text-[11px] text-white/35">{m.sub}</div>
        </div>
      ))}
    </div>
  )
}
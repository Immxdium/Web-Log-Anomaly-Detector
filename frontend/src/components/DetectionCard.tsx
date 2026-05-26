import type { Detection } from '@/types'

interface DetectionCardProps {
  detection: Detection
}

const SEVERITY_STYLES = {
  HIGH:   { badge: 'bg-red-500/20 text-red-400',    icon: 'rgba(255,100,100,0.9)' },
  MEDIUM: { badge: 'bg-yellow-500/20 text-yellow-400', icon: 'rgba(255,190,60,0.9)'  },
  LOW:    { badge: 'bg-emerald-500/20 text-emerald-400', icon: 'rgba(60,220,140,0.9)' },
}

export function DetectionCard({ detection }: DetectionCardProps) {
  const style = SEVERITY_STYLES[detection.severity]

  if (detection.count === 0) return null

  return (
    <div className="liquid-glass flex flex-col gap-4 rounded-[20px] p-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div
          className="liquid-glass flex h-10 w-10 flex-shrink-0
                     items-center justify-center rounded-[10px]"
        >
          <DetectionIcon name={detection.key} color={style.icon} />
        </div>
        <div
          className="flex-1 text-xl leading-tight tracking-[-0.5px] text-white"
          style={{ fontFamily: 'Instrument Serif, serif', fontStyle: 'italic' }}
        >
          {detection.title}
        </div>
        <span
          className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold
                      uppercase tracking-wider ${style.badge}`}
        >
          {detection.severity}
        </span>
      </div>

      {/* Count */}
      <div className="text-sm text-white/40">
        {detection.count} event{detection.count !== 1 ? 's' : ''} detected
      </div>

      {/* Table */}
      {detection.data.length > 0 && (
        <table className="w-full border-collapse text-xs">
          <thead>
            <tr>
              {detection.columns.map((col) => (
                <th
                  key={col}
                  className="border-b border-white/8 pb-2 text-left
                             text-[10px] font-normal uppercase tracking-wider
                             text-white/30"
                  style={{ textAlign: col === detection.columns[detection.columns.length - 1] ? 'right' : 'left' }}
                >
                  {col.replace(/_/g, ' ')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {detection.data.slice(0, 3).map((row, i) => (
              <tr key={i} className="border-b border-white/4">
                {detection.columns.map((col, j) => (
                  <td
                    key={col}
                    className="py-1.5"
                    style={{
                      textAlign: j === detection.columns.length - 1 ? 'right' : 'left',
                      color: j === 0
                        ? 'rgba(180,120,255,0.9)'
                        : 'rgba(255,255,255,0.45)',
                      fontWeight: j === 0 ? 500 : 400,
                      maxWidth: '160px',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {j === detection.columns.length - 1 ? (
                      <span
                        className={`rounded-full px-2 py-0.5 text-[11px]
                                    font-semibold ${style.badge}`}
                      >
                        {String(row[col])}
                      </span>
                    ) : (
                      String(row[col])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

/* Maps detection key → icon SVG */
function DetectionIcon({ name, color }: { name: string; color: string }) {
  const props = { width: 18, height: 18, viewBox: '0 0 24 24',
                  fill: 'none', stroke: color, strokeWidth: 2 }
  switch (name) {
    case 'sqli':
      return <svg {...props}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
    case 'scanner_agents':
      return <svg {...props}><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    case 'brute_force':
      return <svg {...props}><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
    case 'sensitive_paths':
      return <svg {...props}><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
    case 'xss':
      return <svg {...props}><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
    case 'path_traversal':
      return <svg {...props}><polyline points="9 18 3 12 9 6"/><polyline points="15 6 21 12 15 18"/></svg>
    case 'high_volume':
      return <svg {...props}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
    case 'error_spike':
      return <svg {...props}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
    default:
      return <svg {...props}><circle cx="12" cy="12" r="10"/></svg>
  }
}
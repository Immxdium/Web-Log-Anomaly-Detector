interface FooterProps {
    onExport: () => void
    hasResults: boolean
  }
  
  export function Footer({ onExport, hasResults }: FooterProps) {
    return (
      <footer className="mt-6 flex items-center justify-between border-t
                         border-white/6 px-8 py-6">
        <div className="flex items-center gap-8">
          <span
            className="text-2xl text-white"
            style={{ fontFamily: 'Instrument Serif, serif', fontStyle: 'italic' }}
          >
            wlad
          </span>
          <span
            className="text-lg text-white/35"
            style={{ fontFamily: 'Instrument Serif, serif', fontStyle: 'italic' }}
          >
            Axiom · Vanguard · Cipher · Sentry · Recon
          </span>
        </div>
  
        <div className="flex items-center gap-4">
          {hasResults && (
            <button
              onClick={onExport}
              className="border-none bg-transparent text-xs
                         text-white/40 transition-colors hover:text-white/80"
            >
              Export JSON
            </button>
          )}
          <div className="flex items-center gap-1.5 rounded-full
                          bg-red-500/20 px-2.5 py-1 text-[10px]
                          font-bold uppercase tracking-wider text-red-400">
            <span className="live-dot h-1.5 w-1.5 rounded-full bg-red-400" />
            Live
          </div>
        </div>
      </footer>
    )
  }
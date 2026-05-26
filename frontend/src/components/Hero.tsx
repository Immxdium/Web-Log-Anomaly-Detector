interface HeroProps {
    onScrollToUpload: () => void
}

export function Hero({ onScrollToUpload }: HeroProps) {
    return (
        <section
          className="relative flex min-h-screen flex-col overflow-hidden"
          style={{
            background: 'linear-gradient(160deg, #050510 0%, #000 50%, #080818 100%)',
          }}
        >
          {/* Dot grid */}
          <div
            className="pointer-events-none absolute inset-0"
            style={{
                backgroundImage: 'radial-gradient(rgba(120,80,255,0.12) 1px, transparent 1px)',
                backgroundSize: '40px 40px',
            }}
          />
          {/* Purple glow */}
          <div
            className="pointer-events-none absolute left-1/2 -translate-x-1/2"
            style={{
              top: '-200px', width: '800px', height: '600px',
              background: 'radial-gradient(ellipse, rgba(100,60,240,0.18) 0%, transparent 65%)',
            }}
          />
          {/* Red glow */}
          <div
            className="pointer-events-none absolute -bottom-24 -right-24"
            style={{
              width: '500px', height: '400px',
              background: 'radial-gradient(ellipse, rgba(220,50,50,0.1) 0%, transparent 65%)',
            }}
          />

          {/* Content */}
          <div className="relative z-10 flex flex-1 flex-col items-center justify-center px-6 pb-10 pt-20 text-center">
            {/* Badge */}
            <div className="liquid-glass mb-6 inline-flex items-center gap-2 rounded-full py-1.5 pl-1.5 pr-4">
              <span className="rounded-full bg-purple-500/90 px-2.5 py-0.5 text-xs font-medium">
                Live
              </span>
              <span className="text-sm text-white/85">
                Analyzing 2,847 log entries in real-time
              </span>
            </div>

            {/* Headline */}
            <h1
              className="mb-5 max-w-2xl leading-[0.85] tracking-[-3px] text-white"
              style={{
                fontFamily: 'Instrument Serif, serif',
                fontStyle: 'italic',
                fontSize: 'clamp(3.2rem, 7vw, 6rem)',
              }}
            >
              Detect{' '}
              <span style={{ color: 'rgba(180,120,255,0.9)' }}>Threats</span>
              <br />
              Before They Strike
            </h1>

            {/* Subheadline */}
            <p className="mb-8 max-w-xl text-sm font-light leading-relaxed text-white/60 md:text-base">
            Drop any Apache or Nginx access log and instantly surface SQLi, XSS,
            brute force, path traversal, and scanner activity — color-coded by
            severity.
            </p>

            {/* CTAs */}
            <div className="mb-12 flex items-center gap-6">
              <button
                type="button"
                onClick={onScrollToUpload}
                className="liquid-glass-strong flex cursor-pointer items-center
                           gap-2 rounded-full border-none px-5 py-2.5 text-sm
                           font-medium text-white"
              >
                <UploadIcon />
                Upload Log File
              </button>
              <button
                type="button"
                className="flex cursor-pointer items-center gap-2 border-none
                           bg-transparent text-sm text-white/70 transition-colors
                           hover:text-white"
              >
                <PlayIcon />
                View Sample Report
              </button>
            </div>

            {/* Stat cards */}
            <div className="flex gap-4">
              <div className="liquid-glass flex w-48 flex-col gap-2.5 rounded-[20px] p-5">
                <ClockIcon />
                <div
                  className="text-4xl leading-none tracking-[-1px] text-white"
                  style={{ fontFamily: 'Instrument Serif, serif', fontStyle: 'italic' }}
                >
                  50k
                </div>
                <div className="text-xs font-light text-white/50">
                  Lines parsed per second
                </div>
              </div>
              <div className="liquid-glass flex w-48 flex-col gap-2.5 rounded-[20px] p-5">
                <ShieldIcon />
                <div
                  className="text-4xl leading-none tracking-[-1px] text-white"
                  style={{ fontFamily: 'Instrument Serif, serif', fontStyle: 'italic' }}
                >
                  8
                </div>
                <div className="text-xs font-light text-white/50">
                  Detection rules active
                </div>
              </div>
            </div>
          </div>
        </section>
    )
}

/* ── Inline SVG icons ── */
function UploadIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth="2" strokeLinecap="round">
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
      <polyline points="17 8 12 3 7 8"/>
      <line x1="12" y1="3" x2="12" y2="15"/>
    </svg>
  )
}
function PlayIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <polygon points="6 4 20 12 6 20 6 4"/>
    </svg>
  )
}
function ClockIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
         stroke="rgba(255,255,255,0.8)" strokeWidth="1.5">
      <circle cx="12" cy="12" r="10"/>
      <polyline points="12 6 12 12 16 14"/>
    </svg>
  )
}
function ShieldIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
         stroke="rgba(255,255,255,0.8)" strokeWidth="1.5">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  )
}
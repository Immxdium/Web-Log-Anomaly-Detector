import { DetectionCard } from '@/components/DetectionCard'
import { Footer } from '@/components/Footer'
import { Hero } from '@/components/Hero'
import { Navbar } from '@/components/Navbar'
import { SummaryPanel } from '@/components/SummaryPanel'
import { UploadZone } from '@/components/UploadZone'
import { api } from '@/lib/api'
import type { AnalyzeResponse } from '@/types'
import { isAxiosError } from 'axios'
import { useRef, useState } from 'react'

export default function App() {
  const [results, setResults]   = useState<AnalyzeResponse | null>(null)
  const [loading, setLoading]   = useState(false)
  const [error,   setError]     = useState<string | null>(null)
  const uploadRef               = useRef<HTMLDivElement>(null)

  async function handleFile(file: File) {
    setLoading(true)
    setError(null)
    try {
      const data = await api.analyze(file)
      setResults(data)
      setTimeout(() => {
        uploadRef.current?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    } catch (e: unknown) {
      const detail = isAxiosError<{ detail?: string }>(e)
        ? e.response?.data?.detail
        : undefined
      setError(detail ?? 'Something went wrong. Check the log format.')
    } finally {
      setLoading(false)
    }
  }

  function handleExport() {
    if (!results) return
    const blob = new Blob([JSON.stringify(results, null, 2)], {
      type: 'application/json',
    })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = url
    a.download = 'wlad-report.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-black">
      <Navbar />

      <Hero onScrollToUpload={() =>
        uploadRef.current?.scrollIntoView({ behavior: 'smooth' })
      } />

      {/* Divider */}
      <div className="mx-8 h-px"
           style={{ background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent)' }} />

      {/* Upload + Results */}
      <div ref={uploadRef} className="relative z-10">
        <UploadZone onFile={handleFile} loading={loading} />

        {error && (
          <div className="mx-8 mb-6 rounded-2xl bg-red-500/10 px-5 py-4
                          text-sm text-red-400 border border-red-500/20">
            {error}
          </div>
        )}

        {results && (
          <div className="px-8 pb-16">
            {/* Section header */}
            <div className="mb-1 text-xs uppercase tracking-widest text-white/50">
              // Live Analysis
            </div>
            <h2
              className="mb-8 leading-[0.9] tracking-[-2px] text-white"
              style={{
                fontFamily: 'Instrument Serif, serif',
                fontStyle: 'italic',
                fontSize: 'clamp(2.4rem, 5vw, 4rem)',
              }}
            >
              Threat<br />Intelligence
            </h2>

            <SummaryPanel summary={results.summary} />

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {results.detections.map((d) => (
                <DetectionCard key={d.key} detection={d} />
              ))}
            </div>
          </div>
        )}
      </div>

      <Footer onExport={handleExport} hasResults={!!results} />
    </div>
  )
}
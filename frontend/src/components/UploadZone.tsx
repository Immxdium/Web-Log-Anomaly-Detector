import { useRef, useState } from 'react'

interface UploadZoneProps {
  onFile: (file: File) => void
  loading: boolean
}

export function UploadZone({ onFile, loading }: UploadZoneProps) {
  const inputRef        = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) onFile(file)
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (file) onFile(file)
  }

  return (
    <div className="px-8 pb-16 relative z-10">
      <input
        id="access-log-upload"
        ref={inputRef}
        type="file"
        accept=".log,.txt"
        className="sr-only"
        onChange={handleChange}
        disabled={loading}
      />
      <label
        htmlFor="access-log-upload"
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={`block cursor-pointer rounded-[20px] border-2 border-dashed p-10
                   text-center transition-all duration-200 ${
                     loading ? 'pointer-events-none opacity-60' : ''
                   }`}
        style={{
          borderColor: dragging
            ? 'rgba(160,100,255,0.5)'
            : 'rgba(255,255,255,0.2)',
          background: dragging
            ? 'rgba(160,100,255,0.04)'
            : 'rgba(255,255,255,0.02)',
        }}
      >
        <svg className="mx-auto mb-3 opacity-40" width="40" height="40"
             viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <div className="mb-1.5 text-base font-medium text-white">
          {loading ? 'Analyzing...' : 'Drop your access.log here'}
        </div>
        <div className="text-sm text-white/40">
          Apache · Nginx · Combined Log Format · up to 100 MB
        </div>
      </label>
    </div>
  )
}
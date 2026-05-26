export function Navbar() {
    const links =['Dashboard', 'Analyze', 'Rules', 'History', 'Settings']

    return (
        <nav className="sticky top-0 z-50 flex items-center justify-between px-8 py-4">
            {/* Logo */}
            <div
              className="liquid-glass flex h-11 w-ll flex-shrink-0 cursor-pointer
                         items-center justify-center rounded-full text-xl text-white"
              style={{ fontFamily: 'Instrument Serif, serif', fontStyle: 'italic' }}
            >
              w  
            </div>

            {/* Nav links */}
            <div className="liquid-glass flex items-center gap-1 rounded-full px-1.5 py-1.5">
                {links.map((link) => (
                    <span
                      key={link}
                      className="cursor-pointer rounded-full px-3.5 py-2 text-sm
                                 font-medium text-white/85 transition-colors
                                 hover:bg-white/10 first:bg-white/12"
                    >
                      {link}  
                    </span>
                ))}
                <button
                  className="ml-1.5 cursor-pointer rounded-full bg-white px-4 py-1.5
                             text-sm font-semibold text-black transition-opacity
                             hover:opacity-90"
                >
                  Upload Log ↗
                  </button>
            </div>

            {/* Spacer mirrors logo */}
            <div className="h-11 w-11 flex-shrink-0" />
        </nav>
    )
}
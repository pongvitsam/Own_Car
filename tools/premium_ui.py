"""Premium dark luxury UI tokens and HTML class upgrades for MyHome CarCare."""

PREMIUM_INLINE_STYLES = """
        :root {
            --bg-base: #0B0D10;
            --bg-elevated: #141820;
            --bg-surface: #1A1F2A;
            --text-primary: #F5F3EE;
            --text-secondary: #A8A29E;
            --text-muted: #78716C;
            --accent: #C9A962;
            --accent-dim: rgba(201, 169, 98, 0.15);
            --accent-glow: rgba(201, 169, 98, 0.35);
            --border-subtle: rgba(245, 243, 238, 0.08);
            --border-medium: rgba(245, 243, 238, 0.12);
            --radius-sm: 0.75rem;
            --radius-md: 1rem;
            --radius-lg: 1.25rem;
            --radius-xl: 1.5rem;
            --radius-2xl: 1.75rem;
            --radius-3xl: 2rem;
            --radius-pill: 9999px;
            --shadow-soft: 0 2px 8px rgba(0, 0, 0, 0.25);
            --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.35), 0 1px 0 rgba(255, 255, 255, 0.04) inset;
            --shadow-lift: 0 12px 40px rgba(0, 0, 0, 0.45);
            --shadow-glow: 0 0 0 2px var(--accent-glow), 0 8px 32px rgba(201, 169, 98, 0.2);
            --glass-bg: rgba(20, 24, 32, 0.88);
            --transition-smooth: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        html {
            -webkit-text-size-adjust: 100%;
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background: var(--bg-base);
        }
        body {
            font-family: 'Manrope', system-ui, sans-serif;
            letter-spacing: 0.01em;
            color: var(--text-primary);
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background: transparent;
        }
        .font-display {
            font-family: 'Cormorant Garamond', Georgia, serif;
        }
        .app-shell {
            width: 100%;
            max-width: 100%;
            margin: 0 auto;
            min-height: 100vh;
            min-height: 100dvh;
            display: flex;
            flex-direction: column;
            background: var(--bg-base);
            padding-left: env(safe-area-inset-left, 0);
            padding-right: env(safe-area-inset-right, 0);
            padding-bottom: env(safe-area-inset-bottom, 0);
        }
        @media (min-width: 640px) {
            .app-shell {
                max-width: 36rem;
                box-shadow: var(--shadow-lift), 0 0 0 1px var(--border-subtle);
                min-height: calc(100dvh - 1rem);
            }
        }
        @media (min-width: 768px) {
            .app-shell { max-width: 42rem; }
        }
        @media (min-width: 1024px) {
            .app-shell {
                max-width: 56rem;
                margin-top: 1rem;
                margin-bottom: 1rem;
                border-radius: var(--radius-3xl);
                overflow: hidden;
                min-height: calc(100dvh - 2rem);
                max-height: calc(100dvh - 2rem);
            }
        }
        /* Dark overrides for common Tailwind classes inside app shell */
        .app-shell .text-slate-800 { color: var(--text-primary) !important; }
        .app-shell .text-slate-700 { color: #E7E5E0 !important; }
        .app-shell .text-slate-600 { color: var(--text-secondary) !important; }
        .app-shell .text-slate-500 { color: var(--text-secondary) !important; }
        .app-shell .text-slate-400 { color: var(--text-muted) !important; }
        .app-shell .text-indigo-950 { color: var(--text-primary) !important; }
        .app-shell .text-indigo-900 { color: #E7E5E0 !important; }
        .app-shell .text-indigo-700 { color: var(--accent) !important; }
        .app-shell .text-indigo-600 { color: var(--accent) !important; }
        .app-shell .bg-white { background-color: var(--bg-elevated) !important; }
        .app-shell .bg-slate-50 { background-color: var(--bg-surface) !important; }
        .app-shell .bg-slate-100 { background-color: rgba(255, 255, 255, 0.06) !important; }
        .app-shell .bg-indigo-50 { background-color: var(--accent-dim) !important; }
        .app-shell .bg-indigo-100 { background-color: rgba(201, 169, 98, 0.2) !important; }
        .app-shell .border-slate-100,
        .app-shell .border-slate-200,
        .app-shell .border-slate-200\\/60,
        .app-shell .border-slate-200\\/80 { border-color: var(--border-subtle) !important; }
        .app-shell .border-indigo-100 { border-color: rgba(201, 169, 98, 0.25) !important; }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: rgba(201, 169, 98, 0.35); border-radius: var(--radius-pill); }
        .glass-header {
            background: linear-gradient(180deg, rgba(20, 24, 32, 0.98) 0%, rgba(11, 13, 16, 0.95) 100%) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-medium);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
        }
        .vehicle-strip {
            background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg-base) 100%);
            border-bottom: 1px solid var(--border-subtle);
        }
        .premium-card {
            border-radius: var(--radius-2xl);
            border: 1px solid var(--border-subtle);
            background: linear-gradient(160deg, var(--bg-elevated) 0%, var(--bg-surface) 100%);
            box-shadow: var(--shadow-card);
            transition: box-shadow var(--transition-smooth);
        }
        .card-accent-bar {
            height: 2px;
            border-radius: var(--radius-pill);
            background: linear-gradient(90deg, transparent, var(--accent), #E8D5A3, transparent);
        }
        .card-accent-bar--emerald {
            background: linear-gradient(90deg, transparent, #34d399, #6ee7b7, transparent);
        }
        .stat-box {
            border-radius: var(--radius-xl);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-subtle);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }
        .stats-hero-card {
            border-radius: var(--radius-xl);
            background: linear-gradient(135deg, #0B0D10 0%, #141820 50%, #1A1F2A 100%);
            box-shadow: inset 0 1px 0 rgba(201, 169, 98, 0.12), var(--shadow-card);
            border: 1px solid rgba(201, 169, 98, 0.2);
        }
        .stats-hero-card::before {
            content: '';
            position: absolute;
            top: 0; left: 8%; right: 8%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0.9;
        }
        .vehicle-card {
            border-radius: var(--radius-2xl);
            transition: all var(--transition-smooth);
            box-shadow: var(--shadow-soft);
        }
        .vehicle-card:not(.vehicle-card--active):hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-card);
        }
        .vehicle-card--active {
            box-shadow: var(--shadow-glow) !important;
            transform: scale(1.01);
        }
        .bottom-nav-wrap {
            padding: 0.5rem 1rem 0.75rem;
            padding-bottom: max(0.75rem, env(safe-area-inset-bottom));
        }
        .bottom-nav-bar {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-medium);
            border-radius: var(--radius-2xl);
            box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.35);
        }
        .btn-primary {
            background: linear-gradient(135deg, #A8893E 0%, var(--accent) 50%, #E8D5A3 100%) !important;
            color: #0B0D10 !important;
            box-shadow: 0 4px 16px rgba(201, 169, 98, 0.3);
            border-radius: var(--radius-xl);
            font-weight: 700;
            transition: all var(--transition-smooth);
        }
        .btn-primary:hover {
            box-shadow: 0 6px 24px rgba(201, 169, 98, 0.4);
            transform: translateY(-1px);
        }
        .btn-secondary {
            border-radius: var(--radius-xl);
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-medium);
            color: var(--text-primary) !important;
            transition: all var(--transition-smooth);
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(201, 169, 98, 0.3);
        }
        .btn-emerald {
            background: linear-gradient(135deg, #047857 0%, #059669 50%, #34d399 100%) !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
            border-radius: var(--radius-xl);
            transition: all var(--transition-smooth);
        }
        .btn-emerald:hover {
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
            transform: translateY(-1px);
        }
        .health-track {
            background: rgba(255, 255, 255, 0.06);
            border-radius: var(--radius-pill);
            height: 0.5rem;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3);
        }
        .health-fill {
            background: linear-gradient(90deg, #34d399 0%, var(--accent) 60%, #E8D5A3 100%);
            border-radius: var(--radius-pill);
            box-shadow: 0 0 12px rgba(201, 169, 98, 0.35);
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .empty-state {
            animation: fade-in 0.35s ease;
            text-align: center;
            padding: 2rem 1.5rem;
            border: 1px dashed rgba(201, 169, 98, 0.25);
            border-radius: var(--radius-2xl);
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-muted);
        }
        .log-card {
            border-radius: var(--radius-xl);
            border: 1px solid var(--border-subtle);
            background: linear-gradient(160deg, var(--bg-elevated) 0%, var(--bg-surface) 100%);
            box-shadow: var(--shadow-soft);
            min-height: 88px;
            transition: box-shadow var(--transition-smooth), transform var(--transition-smooth);
        }
        .log-card:hover {
            box-shadow: var(--shadow-card);
            border-color: rgba(201, 169, 98, 0.15);
        }
        .toast-item {
            border-radius: var(--radius-xl) !important;
            box-shadow: var(--shadow-lift) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        .modal-backdrop {
            background: rgba(0, 0, 0, 0.75) !important;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }
        .modal-sheet-inner {
            width: 100%;
            background: var(--bg-elevated) !important;
            color: var(--text-primary);
            border-radius: var(--radius-3xl) var(--radius-3xl) 0 0 !important;
            box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.5);
            border-top: 1px solid var(--border-medium);
        }
        .modal-dialog-inner {
            background: var(--bg-elevated) !important;
            color: var(--text-primary);
            border-radius: var(--radius-2xl) !important;
            box-shadow: var(--shadow-lift);
            border: 1px solid var(--border-medium);
        }
        .input-premium {
            border-radius: var(--radius-xl);
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid var(--border-medium) !important;
            color: var(--text-primary) !important;
            transition: box-shadow var(--transition-smooth), border-color var(--transition-smooth);
        }
        .input-premium:focus {
            box-shadow: 0 0 0 2px var(--accent-glow);
            border-color: var(--accent) !important;
        }
        .nav-tab {
            position: relative;
            min-height: 3rem;
            transition: color var(--transition-smooth);
        }
        .nav-tab-active {
            color: var(--accent) !important;
        }
        .nav-tab-active::after {
            content: '';
            position: absolute;
            bottom: 4px;
            left: 50%;
            transform: translateX(-50%);
            width: 1.25rem;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            border-radius: var(--radius-pill);
        }
        .fab-primary {
            width: 3.5rem;
            height: 3.5rem;
            border-radius: var(--radius-pill);
            background: linear-gradient(135deg, #A8893E 0%, var(--accent) 100%);
            color: #0B0D10;
            box-shadow: 0 6px 24px rgba(201, 169, 98, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            transition: all var(--transition-smooth);
            border: none;
            cursor: pointer;
        }
        .fab-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 32px rgba(201, 169, 98, 0.5);
        }
        .fab-primary.hidden { display: none !important; }
        .carousel-dots {
            display: flex;
            justify-content: center;
            gap: 0.375rem;
            padding-top: 0.25rem;
        }
        .carousel-dot {
            width: 0.375rem;
            height: 0.375rem;
            border-radius: var(--radius-pill);
            background: rgba(255, 255, 255, 0.15);
            transition: all var(--transition-smooth);
        }
        .carousel-dot--active {
            width: 1.25rem;
            background: var(--accent);
        }
        .status-pill {
            border-radius: var(--radius-pill);
            font-size: 0.625rem;
            font-weight: 700;
            padding: 0.125rem 0.625rem;
            letter-spacing: 0.02em;
        }
        .report-collapsible .report-section-body {
            overflow: hidden;
            transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.25s ease;
        }
        .report-collapsible.report-collapsed .report-section-body {
            max-height: 0 !important;
            opacity: 0;
            pointer-events: none;
        }
        .report-collapsible:not(.report-collapsed) .report-section-body {
            max-height: 2000px;
            opacity: 1;
        }
        .report-collapsible .report-toggle-icon {
            transition: transform var(--transition-smooth);
        }
        .report-collapsible.report-collapsed .report-toggle-icon {
            transform: rotate(-90deg);
        }
        .version-badge {
            background: rgba(201, 169, 98, 0.15);
            color: var(--accent);
            border: 1px solid rgba(201, 169, 98, 0.25);
            border-radius: var(--radius-sm);
            padding: 0.125rem 0.375rem;
        }
        @keyframes custom-pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.9; }
        }
        .urgent-alert { animation: custom-pulse 2s infinite; }
        @keyframes slide-up {
            from { transform: translateY(100%); }
            to { transform: translateY(0); }
        }
        .animate-slide-up {
            animation: slide-up 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @media (min-width: 640px) {
            @keyframes slide-up-center {
                from { transform: translateY(16px) scale(0.98); opacity: 0; }
                to { transform: translateY(0) scale(1); opacity: 1; }
            }
            .modal-sheet-inner.animate-slide-up { animation-name: slide-up-center; }
        }
        #vehicles-carousel {
            -webkit-overflow-scrolling: touch;
            scroll-snap-type: x mandatory;
        }
        #vehicles-carousel > * { scroll-snap-align: start; }
        @media (min-width: 768px) {
            #vehicles-carousel {
                display: grid !important;
                grid-template-columns: repeat(2, 1fr);
                overflow: visible !important;
                scroll-snap-type: none;
                padding-bottom: 0;
                gap: 0.875rem;
            }
            .carousel-dots { display: none; }
        }
        @media (min-width: 1024px) {
            #vehicles-carousel { grid-template-columns: repeat(3, 1fr); }
            .dashboard-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
                align-items: start;
            }
            .dashboard-grid > section { margin-bottom: 0 !important; }
        }
        @media (min-width: 1280px) {
            #vehicles-carousel { grid-template-columns: repeat(4, 1fr); }
        }
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        #log-search-input:focus {
            box-shadow: 0 0 0 2px var(--accent-glow);
            border-color: var(--accent);
        }
        button:active { transform: scale(0.97); }
        #loading-overlay.hidden { display: none !important; }
"""

BODY_REPLACEMENTS = [
    ('<body class="h-full flex flex-col max-w-md mx-auto bg-slate-50 shadow-2xl relative overflow-hidden">',
     '<body class="app-shell relative">'),
    ('class="btn-emerald text-[10px] text-white font-bold px-3 py-2 rounded-xl flex items-center space-x-1 transition-all active:scale-95"',
     'class="btn-emerald text-[10px] text-white font-bold p-2.5 rounded-xl flex items-center justify-center transition-all active:scale-95" title="ตรวจสภาพด่วน"'),
    ('<span>ตรวจสภาพด่วน</span>',
     '<span class="sr-only">ตรวจสภาพด่วน</span>'),
    ('class="bg-white/10 hover:bg-white/15 p-2.5 rounded-xl text-slate-200 transition-all active:scale-95 border border-white/10 backdrop-blur-sm"',
     'class="bg-white/5 hover:bg-white/10 p-2.5 rounded-xl text-[var(--text-secondary)] transition-all active:scale-95 border border-white/10"'),
    ('class="modal-sheet-inner bg-white w-full max-w-md p-5 space-y-4 animate-slide-up"',
     'class="modal-sheet-inner w-full max-w-md p-5 space-y-4 animate-slide-up"'),
    ('class="modal-sheet-inner bg-white w-full max-w-md p-5 space-y-4 max-h-[92vh] overflow-y-auto"',
     'class="modal-sheet-inner w-full max-w-md p-5 space-y-4 max-h-[92vh] overflow-y-auto"'),
    ('class="modal-dialog-inner bg-white w-full max-w-sm p-4 space-y-3.5"',
     'class="modal-dialog-inner w-full max-w-sm p-4 space-y-3.5"'),
    ('class="modal-dialog-inner bg-white w-full max-w-sm p-5 space-y-4"',
     'class="modal-dialog-inner w-full max-w-sm p-5 space-y-4"'),
    ('class="input-premium w-full bg-white border border-slate-200/80 rounded-xl py-2.5 pl-3 pr-8 text-[11px] outline-none focus:ring-1 focus:ring-indigo-500"',
     'class="input-premium w-full rounded-xl py-2.5 pl-3 pr-8 text-[11px] outline-none"'),
    ('class="w-full bg-white border border-slate-200 rounded-xl py-2 pl-3 pr-8 text-[11px] outline-none focus:ring-1 focus:ring-indigo-500"',
     'class="input-premium w-full rounded-xl py-2 pl-3 pr-8 text-[11px] outline-none"'),
    ('class="nav-tab nav-tab-active flex flex-col items-center justify-center w-16 text-indigo-600 transition-all"',
     'class="nav-tab nav-tab-active flex flex-col items-center justify-center w-16 transition-all"'),
    ('class="nav-tab flex flex-col items-center justify-center w-16 text-slate-400 hover:text-indigo-400 transition-all"',
     'class="nav-tab flex flex-col items-center justify-center w-16 text-[var(--text-muted)] hover:text-[var(--accent)] transition-all"'),
    ('class="btn-primary flex-1 text-white text-[11px] font-bold py-2.5 px-3 transition-all flex items-center justify-center gap-1.5 active:scale-95"',
     'class="btn-primary flex-1 text-[11px] font-bold py-2.5 px-3 transition-all flex items-center justify-center gap-1.5 active:scale-95"'),
    ('class="btn-primary w-full text-white font-bold py-3 px-4 text-xs transition-all active:scale-95"',
     'class="btn-primary w-full font-bold py-3 px-4 text-xs transition-all active:scale-95"'),
    ('class="btn-emerald w-full text-white text-[11px] font-bold py-3 px-4 transition-all flex items-center justify-center gap-1.5 active:scale-95"',
     'class="btn-emerald w-full text-[11px] font-bold py-3 px-4 transition-all flex items-center justify-center gap-1.5 active:scale-95"'),
]

SCRIPT_REPLACEMENTS = [
    ('vehicle-card snap-start shrink-0 w-[150px] md:w-auto p-3.5 rounded-2xl border cursor-pointer transition-all duration-300',
     'vehicle-card snap-start shrink-0 w-[85vw] max-w-[320px] md:w-auto p-4 rounded-2xl border cursor-pointer transition-all duration-300'),
    ("? 'vehicle-card vehicle-card--active border-indigo-400/50 bg-gradient-to-br from-indigo-950 via-indigo-900 to-slate-900 text-white ring-2 ring-indigo-400/40' ",
     "? 'vehicle-card vehicle-card--active border-[var(--accent)]/40 bg-gradient-to-br from-[#1A1F2A] via-[#141820] to-[#0B0D10] text-[var(--text-primary)] ring-2 ring-[var(--accent)]/30' "),
    (": 'border-slate-200/80 bg-white hover:border-indigo-200 text-slate-800'",
     ": 'border-[var(--border-subtle)] bg-[var(--bg-elevated)] hover:border-[var(--accent)]/30 text-[var(--text-primary)]'"),
    ('toast-item p-4 rounded-2xl shadow-xl backdrop-blur-sm',
     'toast-item p-4 rounded-2xl shadow-xl backdrop-blur-sm border border-[var(--border-subtle)]'),
    ('log-card p-4 relative overflow-hidden',
     'log-card p-4 relative overflow-hidden min-h-[88px]'),
    ('inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-[10px] font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-100 active:scale-95',
     'inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-[var(--accent)] bg-[var(--accent-dim)] hover:bg-[rgba(201,169,98,0.25)] border border-[rgba(201,169,98,0.3)] active:scale-95'),
    ('inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-[10px] font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-100 active:scale-95',
     'inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-rose-400 bg-rose-950/40 hover:bg-rose-950/60 border border-rose-900/50 active:scale-95'),
    ('bg-gradient-to-r from-indigo-500 to-indigo-600 h-2 rounded-full',
     'bg-gradient-to-r from-[#A8893E] via-[var(--accent)] to-[#E8D5A3] h-2 rounded-full'),
    ('text-center py-6 text-slate-400 text-[10px] font-bold bg-slate-50 border border-slate-200 border-dashed rounded-xl',
     'empty-state text-center py-6 text-[10px] font-bold'),
    ('<i class="fa-solid fa-gas-pump text-3xl text-emerald-200 block"></i>',
     '<i class="fa-solid fa-gas-pump text-4xl text-[var(--accent)]/40 block"></i>'),
    ('<i class="fa-solid fa-wrench text-3xl text-indigo-200 block"></i>',
     '<i class="fa-solid fa-wrench text-4xl text-[var(--accent)]/40 block"></i>'),
]


def apply_premium_html(text, replacements=None):
    replacements = replacements or BODY_REPLACEMENTS
    for old, new in replacements:
        text = text.replace(old, new)
    if '<footer class="bottom-nav-wrap' in text and '</div>\n    </footer>' not in text:
        text = text.replace(
            '<button onclick="switchTab(\'admin\')" class="flex flex-col items-center justify-center w-16 text-slate-400 transition-all" id="nav-admin">',
            '<button onclick="switchTab(\'admin\')" class="nav-tab flex flex-col items-center justify-center w-16 text-[var(--text-muted)] hover:text-[var(--accent)] transition-all" id="nav-admin">',
        )
        text = text.replace(
            '<button onclick="switchTab(\'dashboard\')" class="flex flex-col items-center justify-center w-16 text-indigo-600 transition-all" id="nav-dashboard">',
            '<button onclick="switchTab(\'dashboard\')" class="nav-tab nav-tab-active flex flex-col items-center justify-center w-16 transition-all" id="nav-dashboard">',
        )
        text = text.replace(
            '<button onclick="switchTab(\'fuelio\')" class="flex flex-col items-center justify-center w-16 text-slate-400 transition-all" id="nav-fuelio">',
            '<button onclick="switchTab(\'fuelio\')" class="nav-tab flex flex-col items-center justify-center w-16 text-[var(--text-muted)] hover:text-[var(--accent)] transition-all" id="nav-fuelio">',
        )
        text = text.replace(
            '        </button>\n    </footer>\n\n    <!-- MODAL 1:',
            '        </button>\n        </div>\n    </footer>\n\n    <!-- MODAL 1:',
        )
    return text


def apply_premium_script(text):
    return apply_premium_html(text, SCRIPT_REPLACEMENTS)

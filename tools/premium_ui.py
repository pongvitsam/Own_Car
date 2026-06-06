"""Premium luxury UI tokens and HTML class upgrades for MyHome CarCare."""

PREMIUM_INLINE_STYLES = """
        :root {
            --radius-sm: 0.75rem;
            --radius-md: 1rem;
            --radius-lg: 1.25rem;
            --radius-xl: 1.5rem;
            --radius-2xl: 1.75rem;
            --radius-3xl: 2rem;
            --radius-pill: 9999px;
            --shadow-soft: 0 1px 3px rgba(15, 23, 42, 0.04), 0 6px 16px rgba(15, 23, 42, 0.06);
            --shadow-card: 0 2px 8px rgba(15, 23, 42, 0.04), 0 12px 32px rgba(15, 23, 42, 0.08);
            --shadow-lift: 0 8px 20px rgba(15, 23, 42, 0.08), 0 24px 48px rgba(15, 23, 42, 0.12);
            --shadow-glow: 0 0 0 3px rgba(129, 140, 248, 0.35), 0 12px 40px rgba(79, 70, 229, 0.4);
            --color-gold: #f59e0b;
            --glass-bg: rgba(255, 255, 255, 0.78);
            --transition-smooth: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        html {
            -webkit-text-size-adjust: 100%;
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background: linear-gradient(165deg, #e2e8f0 0%, #f1f5f9 45%, #e8eef5 100%);
        }
        body {
            font-family: 'Itim', 'Inter', sans-serif;
            letter-spacing: 0.01em;
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background: transparent;
        }
        @media (min-width: 640px) {
            html, body { background: linear-gradient(165deg, #dce3ec 0%, #e2e8f0 50%, #d8e0ea 100%); }
        }
        .app-shell {
            width: 100%;
            max-width: 100%;
            margin: 0 auto;
            min-height: 100vh;
            min-height: 100dvh;
            display: flex;
            flex-direction: column;
            background: linear-gradient(180deg, #fafbfc 0%, #f4f6f9 100%);
            padding-left: env(safe-area-inset-left, 0);
            padding-right: env(safe-area-inset-right, 0);
            padding-bottom: env(safe-area-inset-bottom, 0);
        }
        @media (min-width: 640px) {
            .app-shell {
                max-width: 36rem;
                box-shadow: var(--shadow-lift), 0 0 0 1px rgba(255, 255, 255, 0.6);
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
        @media (min-width: 1280px) {
            .app-shell { max-width: 64rem; }
        }
        @media (min-width: 1536px) {
            .app-shell { max-width: 80rem; }
        }
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; border-radius: var(--radius-pill); }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #cbd5e1, #94a3b8); border-radius: var(--radius-pill); }
        .glass-header {
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.97) 0%, rgba(15, 23, 42, 0.95) 50%, rgba(30, 27, 75, 0.97) 100%) !important;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 24px rgba(15, 23, 42, 0.22);
        }
        .vehicle-strip {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.96) 0%, rgba(248, 250, 252, 0.92) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(226, 232, 240, 0.65);
        }
        .premium-card {
            border-radius: var(--radius-2xl);
            border: 1px solid rgba(226, 232, 240, 0.85);
            background: linear-gradient(145deg, #ffffff 0%, #fafbfc 100%);
            box-shadow: var(--shadow-card);
            transition: box-shadow var(--transition-smooth), transform var(--transition-smooth);
        }
        @media (min-width: 1024px) {
            .premium-card:hover {
                box-shadow: var(--shadow-lift);
                transform: translateY(-2px);
            }
        }
        .card-accent-bar {
            height: 3px;
            border-radius: var(--radius-pill);
            background: linear-gradient(90deg, #6366f1 0%, #818cf8 45%, #a5b4fc 100%);
        }
        .card-accent-bar--emerald {
            background: linear-gradient(90deg, #10b981 0%, #34d399 50%, #6ee7b7 100%);
        }
        .stat-box {
            border-radius: var(--radius-xl);
            background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid rgba(226, 232, 240, 0.7);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85);
        }
        .stats-hero-card {
            border-radius: var(--radius-xl);
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 42%, #312e81 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 16px 40px rgba(30, 27, 75, 0.45);
            border: 1px solid rgba(129, 140, 248, 0.22);
        }
        .stats-hero-card::before {
            content: '';
            position: absolute;
            top: 0; left: 10%; right: 10%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--color-gold), #fbbf24, transparent);
            opacity: 0.75;
        }
        .vehicle-card {
            border-radius: var(--radius-2xl);
            transition: all var(--transition-smooth);
            box-shadow: var(--shadow-soft);
        }
        .vehicle-card:not(.vehicle-card--active):hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-card);
        }
        .vehicle-card--active {
            box-shadow: var(--shadow-glow) !important;
            transform: scale(1.02);
        }
        .bottom-nav-wrap {
            padding: 0.5rem 1rem 0.75rem;
            padding-bottom: max(0.75rem, env(safe-area-inset-bottom));
        }
        .bottom-nav-bar {
            background: var(--glass-bg);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(226, 232, 240, 0.92);
            border-radius: var(--radius-2xl);
            box-shadow: 0 -2px 20px rgba(15, 23, 42, 0.06), 0 8px 32px rgba(15, 23, 42, 0.08);
        }
        .btn-primary {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #818cf8 100%) !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
            border-radius: var(--radius-xl);
            transition: all var(--transition-smooth);
        }
        .btn-primary:hover {
            background: linear-gradient(135deg, #4338ca 0%, #4f46e5 50%, #6366f1 100%) !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45);
            transform: translateY(-1px);
        }
        .btn-secondary {
            border-radius: var(--radius-xl);
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            transition: all var(--transition-smooth);
        }
        .btn-secondary:hover {
            background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
            box-shadow: var(--shadow-soft);
        }
        .btn-emerald {
            background: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%) !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
            border-radius: var(--radius-xl);
            transition: all var(--transition-smooth);
        }
        .btn-emerald:hover {
            background: linear-gradient(135deg, #047857 0%, #059669 50%, #10b981 100%) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
            transform: translateY(-1px);
        }
        .health-track {
            background: linear-gradient(90deg, #e2e8f0, #f1f5f9);
            border-radius: var(--radius-pill);
            height: 0.5rem;
            box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.08);
        }
        .health-fill {
            background: linear-gradient(90deg, #34d399 0%, #10b981 30%, #6366f1 75%, #818cf8 100%);
            border-radius: var(--radius-pill);
            box-shadow: 0 0 12px rgba(52, 211, 153, 0.35);
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .empty-state {
            animation: fade-in 0.35s ease;
            text-align: center;
            padding: 2rem 1.5rem;
            border: 2px dashed rgba(203, 213, 225, 0.85);
            border-radius: var(--radius-2xl);
            background: linear-gradient(145deg, #fafbfc 0%, #f8fafc 100%);
        }
        .log-card {
            border-radius: var(--radius-xl);
            border: 1px solid rgba(226, 232, 240, 0.8);
            background: linear-gradient(145deg, #ffffff 0%, #fafbfc 100%);
            box-shadow: var(--shadow-soft);
            transition: box-shadow var(--transition-smooth), transform var(--transition-smooth);
        }
        .log-card:hover {
            box-shadow: var(--shadow-card);
            transform: translateY(-1px);
        }
        .toast-item {
            border-radius: var(--radius-xl) !important;
            box-shadow: var(--shadow-lift) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        .modal-backdrop {
            background: rgba(15, 23, 42, 0.68) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        .modal-sheet-inner {
            width: 100%;
            border-radius: var(--radius-3xl) var(--radius-3xl) 0 0 !important;
            box-shadow: 0 -8px 40px rgba(15, 23, 42, 0.15);
        }
        .modal-dialog-inner {
            border-radius: var(--radius-2xl) !important;
            box-shadow: var(--shadow-lift);
        }
        .input-premium {
            border-radius: var(--radius-xl);
            transition: box-shadow var(--transition-smooth), border-color var(--transition-smooth);
        }
        .input-premium:focus {
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
            border-color: #a5b4fc;
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
            .tab-content > section { transition: box-shadow var(--transition-smooth); }
        }
        @media (min-width: 1280px) {
            #vehicles-carousel { grid-template-columns: repeat(4, 1fr); }
        }
        .nav-tab { position: relative; min-height: 3rem; transition: color var(--transition-smooth); }
        .nav-tab-active::after {
            content: '';
            position: absolute;
            bottom: 4px;
            width: 1.5rem;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #818cf8, #f59e0b);
            border-radius: var(--radius-pill);
        }
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        #log-search-input:focus {
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
            border-color: #a5b4fc;
        }
        button:active { transform: scale(0.97); }
        #loading-overlay.hidden { display: none !important; }
"""

BODY_REPLACEMENTS = [
    ('<header class="bg-gradient-to-r from-indigo-950 via-slate-900 to-indigo-950 text-white px-4 py-3.5 sticky top-0 z-50 shadow-md">',
     '<header class="glass-header text-white px-4 py-4 sticky top-0 z-50">'),
    ('class="bg-emerald-600 hover:bg-emerald-500 text-[10px] text-white font-bold px-2.5 py-1.5 rounded-lg flex items-center space-x-1 transition-all active:scale-95 shadow-sm"',
     'class="btn-emerald text-[10px] text-white font-bold px-3 py-2 rounded-xl flex items-center space-x-1 transition-all active:scale-95"'),
    ('class="bg-slate-800 hover:bg-slate-700 p-2.5 rounded-lg text-slate-300 transition-all active:scale-95 border border-slate-700" title="ดู LINE Log"',
     'class="bg-white/10 hover:bg-white/15 p-2.5 rounded-xl text-slate-200 transition-all active:scale-95 border border-white/10 backdrop-blur-sm" title="ดู LINE Log"'),
    ('<section class="bg-white p-3.5 border-b border-slate-200/60 shadow-sm space-y-3 shrink-0">',
     '<section class="vehicle-strip p-4 space-y-3 shrink-0">'),
    ('id="tab-dashboard" class="tab-content flex-1 overflow-y-auto p-4 space-y-4"',
     'id="tab-dashboard" class="tab-content flex-1 overflow-y-auto p-5 space-y-5"'),
    ('id="tab-fuelio" class="tab-content flex-1 overflow-y-auto p-4 space-y-4 hidden"',
     'id="tab-fuelio" class="tab-content flex-1 overflow-y-auto p-5 space-y-5 hidden"'),
    ('id="tab-admin" class="tab-content flex-1 overflow-y-auto p-4 space-y-4 hidden"',
     'id="tab-admin" class="tab-content flex-1 overflow-y-auto p-5 space-y-5 hidden"'),
    ('<section class="bg-white p-4 rounded-2xl border border-slate-200/60 shadow-sm space-y-3.5 relative overflow-hidden">\n            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-blue-500"></div>',
     '<section class="premium-card p-5 space-y-4 relative overflow-hidden">\n            <div class="absolute top-0 left-0 right-0 card-accent-bar"></div>'),
    ('class="bg-slate-50 p-3 rounded-xl border border-slate-100 relative"', 'class="stat-box p-3.5 relative"'),
    ('class="bg-slate-50 p-3 rounded-xl border border-slate-100"', 'class="stat-box p-3.5"'),
    ('<div class="p-3 bg-gradient-to-r from-slate-50 to-indigo-50/30 rounded-xl border border-slate-100 space-y-2 text-xs">',
     '<div class="p-3.5 bg-gradient-to-r from-slate-50 to-indigo-50/40 rounded-2xl border border-slate-100/80 space-y-2 text-xs">'),
    ('<div class="w-full bg-slate-100 rounded-full h-1.5">\n                        <div id="car-health-bar" class="bg-gradient-to-r from-emerald-400 to-indigo-600 h-1.5 rounded-full transition-all duration-500" style="width: 100%"></div>\n                    </div>',
     '<div class="health-track w-full">\n                        <div id="car-health-bar" class="health-fill h-2" style="width: 100%"></div>\n                    </div>'),
    ('class="flex-1 bg-white hover:bg-slate-50 text-slate-700 text-[11px] font-bold py-2.5 px-3 rounded-xl border border-slate-200 transition-all flex items-center justify-center gap-1.5 shadow-sm active:scale-95"',
     'class="btn-secondary flex-1 text-slate-700 text-[11px] font-bold py-2.5 px-3 border border-slate-200/80 transition-all flex items-center justify-center gap-1.5 shadow-sm active:scale-95"'),
    ('class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white text-[11px] font-bold py-2.5 px-3 rounded-xl transition-all flex items-center justify-center gap-1.5 shadow-md active:scale-95"',
     'class="btn-primary flex-1 text-white text-[11px] font-bold py-2.5 px-3 transition-all flex items-center justify-center gap-1.5 active:scale-95"'),
    ('<section class="bg-white p-4 rounded-2xl border border-slate-200/60 shadow-sm space-y-4">', '<section class="premium-card p-5 space-y-4">'),
    ('<section class="bg-white p-4 rounded-2xl border border-slate-200/60 shadow-sm space-y-4 relative overflow-hidden">\n            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 to-teal-400"></div>',
     '<section class="premium-card p-5 space-y-4 relative overflow-hidden">\n            <div class="absolute top-0 left-0 right-0 card-accent-bar card-accent-bar--emerald"></div>'),
    ('class="bg-gradient-to-br from-slate-900 to-indigo-950 text-white p-4 rounded-xl flex justify-between items-center relative overflow-hidden shadow-inner"',
     'class="stats-hero-card text-white p-5 flex justify-between items-center relative overflow-hidden"'),
    ('class="w-full bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold py-3 px-4 rounded-xl transition-all flex items-center justify-center gap-1.5 shadow-md shadow-emerald-100 active:scale-95"',
     'class="btn-emerald w-full text-white text-[11px] font-bold py-3 px-4 transition-all flex items-center justify-center gap-1.5 active:scale-95"'),
    ('id="admin-tab-auth-view" class="bg-white p-5 rounded-2xl border border-slate-200/60 shadow-sm space-y-4"',
     'id="admin-tab-auth-view" class="premium-card p-6 space-y-4"'),
    ('class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl text-xs transition-all active:scale-95 shadow-md"',
     'class="btn-primary w-full text-white font-bold py-3 px-4 text-xs transition-all active:scale-95"'),
    ('<footer class="bg-white border-t border-slate-100 h-16 flex items-center justify-around px-2 sticky bottom-0 z-40 shadow-[0_-4px_12px_rgba(0,0,0,0.03)] shrink-0">',
     '<footer class="bottom-nav-wrap sticky bottom-0 z-40 shrink-0">\n        <div class="bottom-nav-bar flex items-center justify-around h-16 px-2">'),
    ('id="odometer-modal" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-end justify-center">',
     'id="odometer-modal" class="modal-backdrop hidden fixed inset-0 z-50 flex items-end justify-center">'),
    ('id="repair-modal" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-end justify-center overflow-y-auto">',
     'id="repair-modal" class="modal-backdrop hidden fixed inset-0 z-50 flex items-end justify-center overflow-y-auto">'),
    ('id="fuel-modal" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-end justify-center overflow-y-auto">',
     'id="fuel-modal" class="modal-backdrop hidden fixed inset-0 z-50 flex items-end justify-center overflow-y-auto">'),
    ('id="line-logs-modal" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">',
     'id="line-logs-modal" class="modal-backdrop hidden fixed inset-0 z-50 flex items-center justify-center p-4">'),
    ('id="edit-log-modal" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">',
     'id="edit-log-modal" class="modal-backdrop hidden fixed inset-0 z-50 flex items-center justify-center p-4">'),
    ('class="bg-white w-full max-w-md rounded-t-3xl p-5 space-y-4 animate-slide-up shadow-2xl"',
     'class="modal-sheet-inner bg-white w-full max-w-md p-5 space-y-4 animate-slide-up"'),
    ('class="bg-white w-full max-w-md rounded-t-3xl p-5 space-y-4 shadow-2xl max-h-[92vh] overflow-y-auto"',
     'class="modal-sheet-inner bg-white w-full max-w-md p-5 space-y-4 max-h-[92vh] overflow-y-auto"'),
    ('class="bg-white w-full max-w-sm rounded-2xl p-4 space-y-3.5 shadow-2xl"',
     'class="modal-dialog-inner bg-white w-full max-w-sm p-4 space-y-3.5"'),
    ('class="bg-white w-full max-w-sm rounded-2xl p-5 space-y-4 shadow-2xl"',
     'class="modal-dialog-inner bg-white w-full max-w-sm p-5 space-y-4"'),
    ('class="w-full bg-white border border-slate-200 rounded-xl py-2 pl-3 pr-8 text-[11px] outline-none focus:ring-1 focus:ring-indigo-500"',
     'class="input-premium w-full bg-white border border-slate-200/80 rounded-xl py-2.5 pl-3 pr-8 text-[11px] outline-none focus:ring-1 focus:ring-indigo-500"'),
    ('class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl transition-all shadow-md active:scale-95 text-xs"',
     'class="btn-primary w-full text-white font-bold py-3 px-4 transition-all active:scale-95 text-xs"'),
    ('class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 rounded-xl transition-all shadow-md">บันทึกที่แก้ไข</button>',
     'class="flex-1 btn-primary text-white font-bold py-2 transition-all">บันทึกที่แก้ไข</button>'),
]

SCRIPT_REPLACEMENTS = [
    ('rounded-lg px-2 py-1 outline-none focus:ring-1 focus:ring-indigo-500',
     'rounded-xl px-2.5 py-1.5 outline-none focus:ring-2 focus:ring-indigo-500/40'),
    ('vehicle-card snap-start shrink-0 w-[145px] md:w-auto p-3 rounded-xl border',
     'vehicle-card snap-start shrink-0 w-[150px] md:w-auto p-3.5 rounded-2xl border transition-all duration-300'),
    ("? 'vehicle-card vehicle-card--active border-indigo-500 bg-gradient-to-br from-indigo-900 to-indigo-950 text-white shadow-lg ring-2 ring-indigo-400/30' ",
     "? 'vehicle-card vehicle-card--active border-indigo-400/50 bg-gradient-to-br from-indigo-950 via-indigo-900 to-slate-900 text-white ring-2 ring-indigo-400/40' "),
    ('toast-item p-3.5 rounded-xl shadow-lg', 'toast-item p-4 rounded-2xl shadow-xl backdrop-blur-sm'),
    ('bg-white p-3.5 rounded-xl border border-slate-200/60 shadow-sm hover:shadow transition-all relative overflow-hidden',
     'log-card p-4 relative overflow-hidden'),
    ('text-center py-6 text-slate-400 text-[10px] font-bold bg-slate-50 border border-slate-200 border-dashed rounded-xl',
     'empty-state text-center py-6 text-slate-400 text-[10px] font-bold'),
]


def apply_premium_html(text, replacements=None):
    replacements = replacements or BODY_REPLACEMENTS
    for old, new in replacements:
        text = text.replace(old, new)
    if '<footer class="bottom-nav-wrap' in text and '</div>\n    </footer>' not in text:
        text = text.replace(
            '<button onclick="switchTab(\'admin\')" class="flex flex-col items-center justify-center w-16 text-slate-400 transition-all" id="nav-admin">',
            '<button onclick="switchTab(\'admin\')" class="nav-tab flex flex-col items-center justify-center w-16 text-slate-400 hover:text-indigo-400 transition-all" id="nav-admin">',
        )
        text = text.replace(
            '<button onclick="switchTab(\'dashboard\')" class="flex flex-col items-center justify-center w-16 text-indigo-600 transition-all" id="nav-dashboard">',
            '<button onclick="switchTab(\'dashboard\')" class="nav-tab nav-tab-active flex flex-col items-center justify-center w-16 text-indigo-600 transition-all" id="nav-dashboard">',
        )
        text = text.replace(
            '<button onclick="switchTab(\'fuelio\')" class="flex flex-col items-center justify-center w-16 text-slate-400 transition-all" id="nav-fuelio">',
            '<button onclick="switchTab(\'fuelio\')" class="nav-tab flex flex-col items-center justify-center w-16 text-slate-400 hover:text-indigo-400 transition-all" id="nav-fuelio">',
        )
        text = text.replace(
            '        </button>\n    </footer>\n\n    <!-- MODAL 1:',
            '        </button>\n        </div>\n    </footer>\n\n    <!-- MODAL 1:',
        )
    return text


def apply_premium_script(text):
    return apply_premium_html(text, SCRIPT_REPLACEMENTS)

"""Premium light Sarabun UI tokens and HTML class upgrades for MyHome CarCare."""

PREMIUM_INLINE_STYLES = """
        :root {
            --bg-base: #F7F8FA;
            --bg-elevated: #FFFFFF;
            --bg-surface: #FFFFFF;
            --text-primary: #1A1D24;
            --text-secondary: #5C6370;
            --text-muted: #94A3B8;
            --accent: #2563EB;
            --accent-dim: rgba(37, 99, 235, 0.1);
            --accent-glow: rgba(37, 99, 235, 0.25);
            --border-subtle: rgba(26, 29, 36, 0.08);
            --border-medium: rgba(26, 29, 36, 0.12);
            --radius-sm: 0.75rem;
            --radius-md: 1rem;
            --radius-lg: 1.25rem;
            --radius-xl: 1.5rem;
            --radius-2xl: 1.75rem;
            --radius-3xl: 2rem;
            --radius-pill: 9999px;
            --shadow-soft: 0 1px 3px rgba(26, 29, 36, 0.06), 0 1px 2px rgba(26, 29, 36, 0.04);
            --shadow-card: 0 2px 8px rgba(26, 29, 36, 0.06), 0 1px 2px rgba(26, 29, 36, 0.04);
            --shadow-lift: 0 12px 40px rgba(26, 29, 36, 0.1);
            --shadow-glow: 0 0 0 2px var(--accent-glow), 0 4px 16px rgba(37, 99, 235, 0.15);
            --glass-bg: rgba(255, 255, 255, 0.92);
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
            font-family: 'Sarabun', system-ui, sans-serif;
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
            font-family: 'Sarabun', system-ui, sans-serif;
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
            position: relative;
        }
        .app-main-column {
            display: flex;
            flex-direction: column;
            flex: 1;
            min-width: 0;
            min-height: 100dvh;
        }
        .sidebar-toggle {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2.5rem;
            height: 2.5rem;
            border-radius: var(--radius-xl);
            border: 1px solid var(--border-medium);
            background: #FFFFFF;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all var(--transition-smooth);
            flex-shrink: 0;
        }
        .sidebar-toggle:hover {
            background: var(--accent-dim);
            color: var(--accent);
            border-color: rgba(37, 99, 235, 0.25);
        }
        .sidebar-backdrop {
            position: fixed;
            inset: 0;
            z-index: 80;
            background: rgba(26, 29, 36, 0.45);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            opacity: 0;
            pointer-events: none;
            transition: opacity var(--transition-smooth);
        }
        .sidebar-backdrop--visible {
            opacity: 1;
            pointer-events: auto;
        }
        body.sidebar-open {
            overflow: hidden;
        }
        .side-nav {
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            z-index: 90;
            width: 16.5rem;
            display: flex;
            flex-direction: column;
            background: var(--bg-elevated);
            border-right: 1px solid var(--border-medium);
            box-shadow: var(--shadow-lift);
            transform: translateX(-105%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding-top: env(safe-area-inset-top, 0);
            padding-bottom: env(safe-area-inset-bottom, 0);
        }
        .side-nav--open {
            transform: translateX(0);
        }
        .side-nav-brand {
            display: flex;
            align-items: center;
            gap: 0.625rem;
            padding: 1rem 1rem 0.875rem;
            border-bottom: 1px solid var(--border-subtle);
        }
        .side-nav-logo {
            width: 2.25rem;
            height: 2.25rem;
            border-radius: var(--radius-xl);
            border: 1px solid rgba(37, 99, 235, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent);
            flex-shrink: 0;
        }
        .side-nav-title {
            font-size: 0.875rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.2;
        }
        .side-nav-close {
            margin-left: auto;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            border: none;
            border-radius: var(--radius-lg);
            background: transparent;
            color: var(--text-muted);
            cursor: pointer;
        }
        .side-nav-close:hover {
            background: #F1F5F9;
            color: var(--text-primary);
        }
        .side-nav-menu {
            flex: 1;
            padding: 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.375rem;
            overflow-y: auto;
        }
        .side-nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            width: 100%;
            padding: 0.75rem 0.875rem;
            border: none;
            border-radius: var(--radius-xl);
            background: transparent;
            color: var(--text-secondary);
            font-size: 0.8125rem;
            font-weight: 700;
            cursor: pointer;
            transition: all var(--transition-smooth);
            text-align: left;
        }
        .side-nav-item i {
            width: 1.125rem;
            text-align: center;
            font-size: 1rem;
        }
        .side-nav-item:hover {
            background: var(--accent-dim);
            color: var(--accent);
        }
        .side-nav-item--active {
            background: linear-gradient(90deg, var(--accent-dim) 0%, rgba(37, 99, 235, 0.04) 100%);
            color: var(--accent);
            box-shadow: inset 3px 0 0 var(--accent);
        }
        .side-nav-actions {
            padding: 0.75rem;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            gap: 0.375rem;
        }
        .side-nav-action {
            display: flex;
            align-items: center;
            gap: 0.625rem;
            width: 100%;
            padding: 0.625rem 0.75rem;
            border-radius: var(--radius-lg);
            border: 1px solid var(--border-subtle);
            background: #F8FAFC;
            color: var(--text-secondary);
            font-size: 0.6875rem;
            font-weight: 700;
            cursor: pointer;
            transition: all var(--transition-smooth);
            text-align: left;
        }
        .side-nav-action:hover {
            border-color: rgba(37, 99, 235, 0.2);
            background: #FFFFFF;
            color: var(--accent);
        }
        .side-nav-action--fuel {
            background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
            border-color: rgba(16, 185, 129, 0.25);
            color: #047857;
        }
        .side-nav-action--fuel:hover {
            background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
            color: #065F46;
        }
        @media (min-width: 640px) {
            .app-shell {
                max-width: 36rem;
                box-shadow: var(--shadow-lift), 0 0 0 1px var(--border-subtle);
                min-height: calc(100dvh - 1rem);
            }
        }
        @media (min-width: 768px) {
            .app-shell {
                flex-direction: row;
                align-items: stretch;
                max-width: 100%;
                width: 100%;
                min-height: 100dvh;
                max-height: none;
                margin: 0;
                border-radius: 0;
                box-shadow: none;
            }
            .app-main-column {
                max-height: 100dvh;
                overflow: hidden;
            }
            .side-nav {
                position: sticky;
                top: 0;
                flex-shrink: 0;
                transform: translateX(0);
                height: 100dvh;
                box-shadow: none;
            }
            .side-nav--open {
                transform: translateX(0);
            }
            .side-nav-close,
            .sidebar-toggle,
            .sidebar-backdrop {
                display: none !important;
            }
            .fab-primary {
                bottom: 5.5rem !important;
            }
        }
        @media (min-width: 768px) and (max-width: 1023px) {
            .app-shell {
                max-width: 42rem;
                margin: 0 auto;
            }
        }
        @media (min-width: 1024px) {
            .app-shell {
                max-width: 72rem;
                margin-top: 1rem;
                margin-bottom: 1rem;
                border-radius: var(--radius-3xl);
                overflow: hidden;
                min-height: calc(100dvh - 2rem);
                max-height: calc(100dvh - 2rem);
                box-shadow: var(--shadow-lift), 0 0 0 1px var(--border-subtle);
            }
            .side-nav {
                height: 100%;
                min-height: calc(100dvh - 2rem);
            }
            .app-main-column {
                max-height: calc(100dvh - 2rem);
            }
        }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: rgba(37, 99, 235, 0.25); border-radius: var(--radius-pill); }
        .glass-header {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-medium);
            box-shadow: 0 1px 3px rgba(26, 29, 36, 0.06);
        }
        .header-fuel-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.375rem;
            min-height: 2.75rem;
            padding: 0.5rem 0.75rem;
            border-radius: var(--radius-xl);
            background: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%);
            color: #fff !important;
            border: none;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
            transition: all var(--transition-smooth);
            cursor: pointer;
        }
        .header-fuel-btn:hover {
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.45);
            transform: translateY(-1px);
        }
        .header-fuel-btn--active {
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.35), 0 4px 14px rgba(16, 185, 129, 0.4);
        }
        .header-fuel-btn.hidden { display: none !important; }
        .vehicle-strip {
            background: linear-gradient(180deg, #FFFFFF 0%, var(--bg-base) 100%);
            border-bottom: 1px solid var(--border-subtle);
        }
        .premium-card {
            border-radius: var(--radius-2xl);
            border: 1px solid var(--border-subtle);
            background: var(--bg-elevated);
            box-shadow: var(--shadow-card);
            transition: box-shadow var(--transition-smooth);
        }
        .card-accent-bar {
            height: 2px;
            border-radius: var(--radius-pill);
            background: linear-gradient(90deg, transparent, var(--accent), #60A5FA, transparent);
        }
        .card-accent-bar--emerald {
            background: linear-gradient(90deg, transparent, #34d399, #6ee7b7, transparent);
        }
        .stat-box {
            border-radius: var(--radius-xl);
            background: #F8FAFC;
            border: 1px solid var(--border-subtle);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
        }
        .stats-hero-card {
            border-radius: var(--radius-xl);
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 50%, #BFDBFE 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8), var(--shadow-card);
            border: 1px solid rgba(37, 99, 235, 0.15);
        }
        .stats-hero-card::before {
            content: '';
            position: absolute;
            top: 0; left: 8%; right: 8%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0.6;
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
            box-shadow: 0 -2px 12px rgba(26, 29, 36, 0.06);
        }
        .btn-primary {
            background: linear-gradient(135deg, #1D4ED8 0%, var(--accent) 50%, #3B82F6 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
            border-radius: var(--radius-xl);
            font-weight: 700;
            transition: all var(--transition-smooth);
        }
        .btn-primary:hover {
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35);
            transform: translateY(-1px);
        }
        .btn-secondary {
            border-radius: var(--radius-xl);
            background: #F8FAFC;
            border: 1px solid var(--border-medium);
            color: var(--text-primary) !important;
            transition: all var(--transition-smooth);
        }
        .btn-secondary:hover {
            background: #F1F5F9;
            border-color: rgba(37, 99, 235, 0.25);
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
            background: #E2E8F0;
            border-radius: var(--radius-pill);
            height: 0.5rem;
            box-shadow: inset 0 1px 2px rgba(26, 29, 36, 0.06);
        }
        .health-fill {
            background: linear-gradient(90deg, #34d399 0%, var(--accent) 60%, #60A5FA 100%);
            border-radius: var(--radius-pill);
            box-shadow: 0 0 8px rgba(37, 99, 235, 0.25);
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .empty-state {
            animation: fade-in 0.35s ease;
            text-align: center;
            padding: 2rem 1.5rem;
            border: 1px dashed rgba(37, 99, 235, 0.2);
            border-radius: var(--radius-2xl);
            background: #F8FAFC;
            color: var(--text-muted);
        }
        .log-card {
            border-radius: var(--radius-xl);
            border: 1px solid var(--border-subtle);
            background: var(--bg-elevated);
            box-shadow: var(--shadow-soft);
            min-height: 88px;
            transition: box-shadow var(--transition-smooth), transform var(--transition-smooth);
        }
        .log-card:hover {
            box-shadow: var(--shadow-card);
            border-color: rgba(37, 99, 235, 0.15);
        }
        .log-list {
            border-radius: var(--radius-xl);
            border: 1px solid var(--border-subtle);
            background: var(--bg-elevated);
            box-shadow: var(--shadow-soft);
            overflow: hidden;
        }
        .log-list .empty-state {
            border: none;
            border-radius: 0;
            background: transparent;
        }
        .log-row {
            padding: 0.5rem 0.625rem;
            border-bottom: 1px solid var(--border-subtle);
            transition: background var(--transition-smooth);
        }
        .log-row:last-child {
            border-bottom: none;
        }
        .log-row:hover {
            background: #F8FAFC;
        }
        .log-row-main {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .log-row-badge {
            flex-shrink: 0;
            max-width: 5.5rem;
            padding: 0.125rem 0.375rem;
            border-radius: 0.375rem;
            font-size: 0.625rem;
            font-weight: 800;
            line-height: 1.2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .log-row-badge--accent {
            background: var(--accent-dim);
            color: var(--accent);
        }
        .log-row-badge--muted {
            background: #F1F5F9;
            color: var(--text-muted);
        }
        .log-row-date {
            font-size: 0.625rem;
            font-weight: 700;
            color: var(--text-muted);
            white-space: nowrap;
        }
        .log-row-title {
            margin-top: 0.125rem;
            font-size: 0.6875rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.25;
        }
        .log-row-meta {
            text-align: right;
            min-width: 4.25rem;
        }
        .log-row-cost {
            font-size: 0.75rem;
            font-weight: 800;
            color: var(--accent);
            font-variant-numeric: tabular-nums;
            line-height: 1.2;
        }
        .log-row-cost--muted {
            color: var(--text-muted);
        }
        .log-row-odo {
            font-size: 0.5625rem;
            font-weight: 700;
            color: var(--text-muted);
            font-variant-numeric: tabular-nums;
        }
        .log-row-actions {
            display: flex;
            align-items: center;
            gap: 0.125rem;
        }
        .log-row-icon-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.625rem;
            height: 1.625rem;
            border-radius: 0.5rem;
            border: none;
            background: transparent;
            color: var(--text-muted);
            cursor: pointer;
            transition: all var(--transition-smooth);
        }
        .log-row-icon-btn:hover {
            background: var(--accent-dim);
            color: var(--accent);
        }
        .log-row-icon-btn--edit:hover {
            background: var(--accent-dim);
            color: var(--accent);
        }
        .log-row-icon-btn--delete:hover {
            background: #FEE2E2;
            color: #DC2626;
        }
        .log-row-extra {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem 0.75rem;
            margin-top: 0.25rem;
            padding-left: 0.125rem;
            font-size: 0.5625rem;
            font-weight: 700;
            color: var(--text-secondary);
        }
        .fuel-list {
            border-radius: var(--radius-xl);
            border: 1px solid var(--border-subtle);
            background: var(--bg-elevated);
            box-shadow: var(--shadow-soft);
            overflow: hidden;
        }
        .fuel-list .empty-state {
            border: none;
            border-radius: 0;
            background: transparent;
        }
        .fuel-row {
            padding: 0.5rem 0.625rem;
            border-bottom: 1px solid var(--border-subtle);
            transition: background var(--transition-smooth);
        }
        .fuel-row:last-child {
            border-bottom: none;
        }
        .fuel-row:hover {
            background: #F8FAFC;
        }
        .fuel-row-main {
            display: flex;
            align-items: center;
            gap: 0.375rem;
        }
        .fuel-row-badge-oil {
            background: #D1FAE5;
            color: #047857;
        }
        .fuel-row-badge-gas {
            background: #FEF3C7;
            color: #B45309;
        }
        .fuel-row-segment {
            display: flex;
            flex-wrap: wrap;
            gap: 0.375rem 0.625rem;
            margin-top: 0.25rem;
            font-size: 0.5625rem;
            font-weight: 700;
        }
        .fuel-segment-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.125rem 0.375rem;
            border-radius: 0.375rem;
            background: #F0FDF4;
            color: #166534;
            border: 1px solid #BBF7D0;
        }
        .fuel-segment-chip--warn {
            background: #FFFBEB;
            color: #B45309;
            border-color: #FDE68A;
        }
        .fuel-segment-chip--muted {
            background: #F8FAFC;
            color: var(--text-muted);
            border-color: var(--border-subtle);
        }
        .fuel-last-fill-card {
            border-color: rgba(16, 185, 129, 0.2);
        }
        .fuel-summary-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.5rem;
        }
        .fuel-summary-stat {
            text-align: center;
            padding: 0.625rem 0.375rem;
            border-radius: var(--radius-xl);
            background: linear-gradient(180deg, #F0FDF4 0%, #ECFDF5 100%);
            border: 1px solid #BBF7D0;
        }
        .fuel-summary-stat-value {
            font-size: 1rem;
            font-weight: 800;
            color: #065F46;
            line-height: 1.2;
        }
        .fuel-summary-stat-label {
            font-size: 0.5625rem;
            font-weight: 700;
            color: #059669;
            margin-top: 0.125rem;
        }
        .fuel-trend-chart {
            display: flex;
            align-items: flex-end;
            gap: 0.375rem;
            min-height: 7rem;
            padding: 0.25rem 0.125rem 0;
        }
        .fuel-trend-col {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            gap: 0.25rem;
            min-width: 0;
            height: 6.5rem;
        }
        .fuel-trend-bar {
            width: 100%;
            max-width: 1.75rem;
            border-radius: 0.5rem 0.5rem 0.25rem 0.25rem;
            min-height: 0.35rem;
            transition: height var(--transition-smooth);
        }
        .fuel-trend-label {
            font-size: 0.5625rem;
            font-weight: 800;
            color: var(--text-secondary);
        }
        .toast-item {
            border-radius: var(--radius-xl) !important;
            box-shadow: var(--shadow-lift) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        .modal-backdrop {
            position: fixed !important;
            inset: 0 !important;
            z-index: 100 !important;
            background: rgba(26, 29, 36, 0.45) !important;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }
        body.modal-open {
            overflow: hidden;
        }
        body.modal-open #app-main {
            overflow: hidden;
        }
        .modal-sheet-inner {
            width: 100%;
            background: var(--bg-elevated) !important;
            color: var(--text-primary);
            border-radius: var(--radius-3xl) var(--radius-3xl) 0 0 !important;
            box-shadow: 0 -8px 40px rgba(26, 29, 36, 0.12);
            border-top: 1px solid var(--border-medium);
        }
        .modal-dialog-inner {
            background: var(--bg-elevated) !important;
            color: var(--text-primary);
            border-radius: var(--radius-2xl) !important;
            box-shadow: var(--shadow-lift);
            border: 1px solid var(--border-medium);
            max-height: min(90dvh, 100%);
            overflow-y: auto;
            overscroll-behavior: contain;
            -webkit-overflow-scrolling: touch;
        }
        .input-premium {
            border-radius: var(--radius-xl);
            background: #FFFFFF !important;
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
            background: linear-gradient(135deg, #1D4ED8 0%, var(--accent) 100%);
            color: #FFFFFF;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.2);
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
            box-shadow: 0 8px 28px rgba(37, 99, 235, 0.45);
        }
        .fab-primary.hidden { display: none !important; }
        #tab-fuelio {
            padding: 0 !important;
        }
        .fuel-top-bar {
            position: sticky;
            top: 0;
            z-index: 25;
            background: linear-gradient(180deg, var(--bg-base) 0%, rgba(247, 248, 250, 0.97) 85%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-subtle);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }
        .fuel-top-cta {
            min-height: 3.25rem;
            text-align: left;
        }
        .fuel-quick-chip {
            min-height: 2.75rem;
            transition: transform var(--transition-smooth), box-shadow var(--transition-smooth);
        }
        .fuel-quick-chip:active {
            transform: scale(0.98);
        }
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
            background: rgba(26, 29, 36, 0.15);
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
            background: var(--accent-dim);
            color: var(--accent);
            border: 1px solid rgba(37, 99, 235, 0.2);
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
     'class="bg-slate-100 hover:bg-slate-200 p-2.5 rounded-xl text-[var(--text-secondary)] transition-all active:scale-95 border border-slate-200"'),
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
     "? 'vehicle-card vehicle-card--active border-[var(--accent)]/40 bg-gradient-to-br from-[#EFF6FF] via-[#DBEAFE] to-[#BFDBFE] text-[var(--text-primary)] ring-2 ring-[var(--accent)]/30' "),
    ("? 'vehicle-card--active border-[var(--accent)]/40 bg-gradient-to-br from-[#1A1F2A] via-[#141820] to-[#0B0D10] text-[var(--text-primary)] ring-2 ring-[var(--accent)]/30' ",
     "? 'vehicle-card--active border-[var(--accent)]/40 bg-gradient-to-br from-[#EFF6FF] via-[#DBEAFE] to-[#BFDBFE] text-[var(--text-primary)] ring-2 ring-[var(--accent)]/30' "),
    (": 'border-slate-200/80 bg-white hover:border-indigo-200 text-slate-800'",
     ": 'border-[var(--border-subtle)] bg-white hover:border-[var(--accent)]/30 text-[var(--text-primary)]'"),
    (": 'border-[var(--border-subtle)] bg-[var(--bg-elevated)] hover:border-[var(--accent)]/30 text-[var(--text-primary)]'",
     ": 'border-[var(--border-subtle)] bg-white hover:border-[var(--accent)]/30 text-[var(--text-primary)]'"),
    ('toast-item p-4 rounded-2xl shadow-xl backdrop-blur-sm',
     'toast-item p-4 rounded-2xl shadow-xl backdrop-blur-sm border border-[var(--border-subtle)]'),
    ('log-card p-4 relative overflow-hidden',
     'log-card p-4 relative overflow-hidden min-h-[88px]'),
    ('inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-[10px] font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-100 active:scale-95',
     'inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-[var(--accent)] bg-[var(--accent-dim)] hover:bg-[rgba(37,99,235,0.15)] border border-[rgba(37,99,235,0.2)] active:scale-95'),
    ('inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-[var(--accent)] bg-[var(--accent-dim)] hover:bg-[rgba(201,169,98,0.25)] border border-[rgba(201,169,98,0.3)] active:scale-95',
     'inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-[var(--accent)] bg-[var(--accent-dim)] hover:bg-[rgba(37,99,235,0.15)] border border-[rgba(37,99,235,0.2)] active:scale-95'),
    ('inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-[10px] font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-100 active:scale-95',
     'inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-200 active:scale-95'),
    ('inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-rose-400 bg-rose-950/40 hover:bg-rose-950/60 border border-rose-900/50 active:scale-95',
     'inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-200 active:scale-95'),
    ('bg-gradient-to-r from-indigo-500 to-indigo-600 h-2 rounded-full',
     'bg-gradient-to-r from-[#1D4ED8] via-[var(--accent)] to-[#60A5FA] h-2 rounded-full'),
    ('bg-gradient-to-r from-[#A8893E] via-[var(--accent)] to-[#E8D5A3] h-2 rounded-full',
     'bg-gradient-to-r from-[#1D4ED8] via-[var(--accent)] to-[#60A5FA] h-2 rounded-full'),
    ('text-center py-6 text-slate-400 text-[10px] font-bold bg-slate-50 border border-slate-200 border-dashed rounded-xl',
     'empty-state text-center py-6 text-[10px] font-bold'),
    ('<i class="fa-solid fa-gas-pump text-3xl text-emerald-200 block"></i>',
     '<i class="fa-solid fa-gas-pump text-4xl text-[var(--accent)]/30 block"></i>'),
    ('<i class="fa-solid fa-wrench text-3xl text-indigo-200 block"></i>',
     '<i class="fa-solid fa-wrench text-4xl text-[var(--accent)]/30 block"></i>'),
    ('<i class="fa-solid fa-gas-pump text-4xl text-[var(--accent)]/40 block"></i>',
     '<i class="fa-solid fa-gas-pump text-4xl text-[var(--accent)]/30 block"></i>'),
    ('<i class="fa-solid fa-wrench text-4xl text-[var(--accent)]/40 block"></i>',
     '<i class="fa-solid fa-wrench text-4xl text-[var(--accent)]/30 block"></i>'),
    ("success: 'bg-gradient-to-r from-indigo-950 to-indigo-900 text-white border-indigo-700/50 shadow-indigo-900/20'",
     "success: 'bg-gradient-to-r from-blue-600 to-blue-500 text-white border-blue-400/50 shadow-blue-500/20'"),
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

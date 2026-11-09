"""Premium light Sarabun UI tokens and HTML class upgrades for MyHome CarCare."""

PREMIUM_INLINE_STYLES = r"""
        :root {
            --bg-base: #F7F8FA;
            --bg-elevated: #FFFFFF;
            --bg-surface: #FFFFFF;
            --text-primary: #1A1D24;
            --text-secondary: #5C6370;
            --text-muted: #94A3B8;
            --accent: #1E2A4A;
            --accent-rgb: 30, 42, 74;
            --accent-dim: rgba(var(--accent-rgb), 0.1);
            --accent-glow: rgba(var(--accent-rgb), 0.25);
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
            --shadow-glow: 0 0 0 2px var(--accent-glow), 0 4px 16px rgba(var(--accent-rgb), 0.15);
            --glass-bg: rgba(255, 255, 255, 0.92);
            --transition-smooth: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        html {
            -webkit-text-size-adjust: 100%;
            width: 100%;
            max-width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background: var(--bg-base);
            overflow-x: clip;
            box-sizing: border-box;
        }
        *, *::before, *::after { box-sizing: inherit; }
        body {
            font-family: system-ui, 'Leelawadee UI', 'Sarabun', sans-serif;
            letter-spacing: 0.01em;
            color: var(--text-primary);
            width: 100%;
            max-width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background: transparent;
            overflow-x: clip;
        }
        .font-display {
            font-family: system-ui, 'Leelawadee UI', 'Sarabun', sans-serif;
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
            border-color: rgba(var(--accent-rgb), 0.25);
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
            border: 1px solid rgba(var(--accent-rgb), 0.25);
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
            background: linear-gradient(90deg, var(--accent-dim) 0%, rgba(var(--accent-rgb), 0.04) 100%);
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
            border-color: rgba(var(--accent-rgb), 0.2);
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
                margin-left: auto;
                margin-right: auto;
                box-shadow: var(--shadow-lift), 0 0 0 1px var(--border-subtle);
                min-height: calc(100dvh - 1rem);
            }
        }
        @media (min-width: 768px) {
            .app-shell {
                max-width: 42rem;
                margin-left: auto;
                margin-right: auto;
            }
            .app-main-column {
                position: relative;
            }
            .fab-primary {
                position: absolute !important;
                bottom: 5.5rem !important;
                right: 1rem !important;
            }
        }
        @media (min-width: 1024px) {
            .app-shell {
                width: calc(100% - 2rem);
                max-width: 64rem;
                margin: 1rem auto;
                border-radius: var(--radius-3xl);
                overflow: hidden;
                min-height: calc(100dvh - 2rem);
                max-height: calc(100dvh - 2rem);
                box-shadow: var(--shadow-lift), 0 0 0 1px var(--border-subtle);
            }
            .app-main-column {
                max-height: calc(100dvh - 2rem);
            }
        }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: rgba(var(--accent-rgb), 0.25); border-radius: var(--radius-pill); }
        .glass-header {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-medium);
            box-shadow: 0 1px 3px rgba(26, 29, 36, 0.06);
        }
        .header-bar {
            display: grid;
            grid-template-columns: auto minmax(0, 1fr) auto;
            align-items: center;
            gap: 0.5rem;
        }
        .header-fuel-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.375rem;
            width: 100%;
            max-width: 16.5rem;
            justify-self: center;
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
        @media (max-width: 639px) {
            .header-fuel-btn { max-width: none; }
        }
        .header-fuel-btn:hover {
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.45);
            transform: translateY(-1px);
        }
        .header-fuel-btn--active {
            box-shadow: 0 0 0 2px rgba(var(--accent-rgb), 0.35), 0 4px 14px rgba(16, 185, 129, 0.4);
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
            background: linear-gradient(90deg, transparent, var(--accent), #6F7C9C, transparent);
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
            border: 1px solid rgba(var(--accent-rgb), 0.15);
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
            flex: 0 0 min(78%, 18rem);
            width: min(78%, 18rem);
            max-width: 100%;
            border-radius: var(--radius-2xl);
            transition: all var(--transition-smooth);
            box-shadow: var(--shadow-soft);
            border: 1px solid var(--border-subtle);
            background: #FFFFFF;
            color: var(--text-primary);
        }
        .vehicle-card:not(.vehicle-card--active):hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-card);
            border-color: rgba(var(--accent-rgb), 0.25);
        }
        .vehicle-card--active {
            box-shadow: var(--shadow-glow) !important;
            transform: scale(1.01);
            border-color: rgba(var(--accent-rgb), 0.4) !important;
            background: linear-gradient(to bottom right, #EFF6FF, #DBEAFE, #BFDBFE) !important;
        }
        .vehicle-card--active .vehicle-card-license {
            color: var(--accent) !important;
        }
        .vehicle-card--active .vehicle-card-name {
            color: var(--text-primary) !important;
        }
        .vehicle-card--active .vehicle-card-odo-wrap {
            border-color: rgba(var(--accent-rgb), 0.2) !important;
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
            background: linear-gradient(135deg, #151E38 0%, var(--accent) 50%, #44527A 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 14px rgba(var(--accent-rgb), 0.25);
            border-radius: var(--radius-xl);
            font-weight: 700;
            transition: all var(--transition-smooth);
        }
        .btn-primary:hover {
            box-shadow: 0 6px 20px rgba(var(--accent-rgb), 0.35);
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
            border-color: rgba(var(--accent-rgb), 0.25);
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
            background: linear-gradient(90deg, #34d399 0%, var(--accent) 60%, #6F7C9C 100%);
            border-radius: var(--radius-pill);
            box-shadow: 0 0 8px rgba(var(--accent-rgb), 0.25);
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .empty-state {
            animation: fade-in 0.35s ease;
            text-align: center;
            padding: 2rem 1.5rem;
            border: 1px dashed rgba(var(--accent-rgb), 0.2);
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
            border-color: rgba(var(--accent-rgb), 0.15);
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
            width: 100%;
            max-width: 28rem;
            box-sizing: border-box;
            max-height: min(90dvh, 100%);
            overflow-x: hidden;
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
            background: linear-gradient(135deg, #151E38 0%, var(--accent) 100%);
            color: #FFFFFF;
            box-shadow: 0 6px 20px rgba(var(--accent-rgb), 0.35), 0 0 0 1px rgba(255, 255, 255, 0.2);
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
            box-shadow: 0 8px 28px rgba(var(--accent-rgb), 0.45);
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
            border: 1px solid rgba(var(--accent-rgb), 0.2);
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
        .dashboard-grid {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }
        .dashboard-grid.space-y-5 > :not([hidden]) ~ :not([hidden]) {
            margin-top: 0 !important;
        }
        #vehicle-pick-panel .premium-card {
            width: 100%;
            max-width: 28rem;
        }
        #repair-form .grid.grid-cols-2,
        #fuel-form .grid.grid-cols-2,
        #odometer-form .grid.grid-cols-2,
        #admin-unlocked-container .grid.grid-cols-2 {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        #fuel-form .grid.grid-cols-3,
        #edit-fuel-modal .grid.grid-cols-3 {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }
        #repair-form .grid > *,
        #fuel-form .grid > *,
        #edit-fuel-modal .grid > *,
        #admin-unlocked-container .grid > * {
            min-width: 0;
        }
        #repair-form input,
        #repair-form select,
        #repair-form button,
        #fuel-form input,
        #fuel-form select,
        #fuel-form button,
        #edit-fuel-modal input,
        #edit-fuel-modal select,
        #edit-fuel-modal button {
            max-width: 100%;
            min-width: 0;
        }
        @media (max-width: 430px) {
            #repair-form .grid.grid-cols-2,
            #fuel-form .grid.grid-cols-2,
            #fuel-form .grid.grid-cols-3,
            #edit-fuel-modal .grid.grid-cols-3,
            #admin-unlocked-container .grid.grid-cols-2 {
                grid-template-columns: minmax(0, 1fr);
            }
        }
        @media (min-width: 768px) {
            .carousel-dots { display: none; }
            #vehicle-pick-panel .premium-card { max-width: 44rem; }
            #vehicle-pick-list {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
                gap: 0.75rem;
            }
        }
        @media (min-width: 1100px) {
            .dashboard-grid {
                display: grid;
                grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
                gap: 1.5rem;
                align-items: stretch;
            }
            .dashboard-grid > section { margin-top: 0 !important; margin-bottom: 0 !important; }
            .dashboard-span-full {
                grid-column: 1 / -1;
            }
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
        html:not(.carcare-authed) #app-main { display: none !important; }
        html.carcare-authed #app-login-screen { display: none !important; }
        html.carcare-picking .vehicle-strip,
        html.carcare-picking .bottom-nav-wrap,
        html.carcare-picking #header-fuel-btn,
        html.carcare-picking #header-ops,
        html.carcare-picking #fab-primary { display: none !important; }
        html.carcare-picking .header-bar { grid-template-columns: 1fr; }
        #app-login-screen {
            position: fixed;
            inset: 0;
            z-index: 200;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100dvh;
            padding: 1.25rem;
            background: var(--bg-base);
        }
        .pwa-install-banner {
            padding: 0 1rem 0.35rem;
            flex-shrink: 0;
        }
        .pwa-install-card {
            display: flex;
            flex-direction: column;
            align-items: stretch;
            gap: 0.5rem;
            padding: 0.7rem 0.8rem;
            background: var(--glass-bg);
            border: 1px solid var(--border-medium);
            border-radius: var(--radius-2xl);
            box-shadow: var(--shadow-card);
        }
        /* ---- Theme: warm ivory, ink navy, brushed-gold hairlines (single layer) ---- */
        .header-fuel-btn { background: var(--accent); box-shadow: 0 2px 8px rgba(var(--accent-rgb), 0.22); font-weight: 600; font-size: 0.9rem; }
        .header-fuel-btn:hover { box-shadow: 0 4px 12px rgba(var(--accent-rgb), 0.3); }
        .btn-primary { background: var(--accent) !important; box-shadow: 0 2px 8px rgba(var(--accent-rgb), 0.22); font-weight: 600; }
        .btn-primary:hover { background: #151E38 !important; transform: none; box-shadow: 0 4px 12px rgba(var(--accent-rgb), 0.3); }
        .btn-primary:disabled, .btn-primary[disabled] { opacity: 0.45; box-shadow: none; cursor: not-allowed; }
        #vehicles-carousel { padding: 3px; margin: -3px; scrollbar-width: none; -webkit-overflow-scrolling: touch; }
        #vehicles-carousel::-webkit-scrollbar { display: none; }
        .vehicle-card:not(.vehicle-card--active):hover { transform: none; box-shadow: var(--shadow-card); }
        .bottom-nav-bar button { border-radius: var(--radius-lg); transition: background var(--transition-smooth), color var(--transition-smooth); }
        .bottom-nav-bar button:active { transform: none; background: var(--accent-dim); }
        button:active { transform: none; }
        .card-accent-bar, .stats-hero-card::before, .nav-tab-active::after { display: none !important; }
        .stat-box { background: #FFFFFF; box-shadow: none; }
        .btn-emerald:hover { background: #047857 !important; transform: none; box-shadow: none; }
        .health-fill { box-shadow: none; }
        .bg-gradient-to-r, .bg-gradient-to-br { background-image: none !important; }
        .from-blue-600 { background-color: #1E2A4A; }
        .from-rose-600, .from-rose-500 { background-color: #E11D48; }
        .from-amber-400 { background-color: #F59E0B; }
        .from-emerald-50 { background-color: #F0FDF7; }
        .from-slate-50 { background-color: #F8FAFC; }
        .from-\[\#1D4ED8\] { background-color: var(--accent); }
        .text-\[7px\] { font-size: 10px; }
        .text-\[9px\] { font-size: 11px; }
        .text-\[10px\] { font-size: 11.5px; }
        .text-\[11px\] { font-size: 12.5px; }
        #header-ops { grid-column: 3; justify-self: end; }
        :root { --shadow-soft: 0 1px 2px rgba(26, 29, 36, 0.05); --shadow-card: 0 1px 2px rgba(27, 31, 42, 0.04), 0 8px 24px rgba(27, 31, 42, 0.04); --shadow-glow: 0 0 0 1px var(--accent), 0 8px 20px rgba(30, 42, 74, 0.12); --border-subtle: rgba(27, 31, 42, 0.07); --bg-base: #F7F5F1; --radius-2xl: 1.375rem; --radius-xl: 1.125rem; --bg-elevated: #FFFFFF; --text-primary: #1B1F2A; --text-secondary: #5B6070; --text-muted: #9097A6; --accent: #1E2A4A;
            --accent-rgb: 30, 42, 74; --accent-dim: rgba(30, 42, 74, 0.07); --accent-glow: rgba(30, 42, 74, 0.2); --gold: #B08D57; --gold-soft: rgba(176, 141, 87, 0.14); --border-medium: rgba(27, 31, 42, 0.11); --radius-lg: 1rem; }
        html, body, .app-shell { background: var(--bg-base); }
        body { line-height: 1.55; letter-spacing: 0; -webkit-font-smoothing: antialiased; font-weight: 400; color: var(--text-primary); }
        h1, h2, h3, h4 { letter-spacing: 0.01em; }
        .glass-header { background: rgba(247, 245, 241, 0.88) !important; box-shadow: none; border-bottom: 1px solid var(--border-subtle); padding-top: max(0.625rem, env(safe-area-inset-top)); }
        .glass-header h1 { font-weight: 600; letter-spacing: 0.04em; }
        .glass-header .w-9 { background: var(--accent); border-color: var(--accent); color: var(--gold); border-radius: 0.75rem; }
        .version-badge { background: transparent; border: 1px solid var(--gold-soft); color: var(--gold); border-radius: 999px; padding: 0 0.5rem; }
        .vehicle-strip { background: transparent; border-bottom: 1px solid var(--border-subtle); }
        .premium-card { border: 1px solid var(--border-subtle); box-shadow: var(--shadow-card); border-radius: var(--radius-2xl); background: #FFFFFF; padding-top: 0; }
        .vehicle-card { flex: 0 0 auto; width: 11.5rem; box-shadow: none; border: 1px solid var(--border-subtle); background: #FFFFFF; border-color: var(--border-subtle); }
        .vehicle-card--active { transform: none; background: #FFFFFF !important; border-color: var(--accent) !important; box-shadow: 0 0 0 1px var(--accent), 0 10px 24px rgba(30, 42, 74, 0.1) !important; }
        .vehicle-card--active .vehicle-card-license { color: var(--gold) !important; }
        .vehicle-card-odo-wrap span:last-child { color: var(--accent); font-weight: 600; }
        .btn-primary, .header-fuel-btn { box-shadow: 0 6px 16px rgba(30, 42, 74, 0.18); background: var(--accent) !important; color: #FFFFFF !important; border-radius: 999px; font-weight: 600; letter-spacing: 0.02em; }
        .btn-primary:hover, .header-fuel-btn:hover { box-shadow: 0 8px 20px rgba(30, 42, 74, 0.24); background: #151E38 !important; }
        .header-fuel-btn i { color: var(--gold); }
        .btn-secondary { background: #FFFFFF; font-weight: 500; border-radius: 999px; border: 1px solid var(--border-medium); }
        .btn-emerald { background: #17803D !important; box-shadow: none; border-radius: 0.875rem; }
        .stat-box, .stats-hero-card { background: #FBFAF8; border: 1px solid var(--border-subtle); box-shadow: none; }
        .stats-hero-card { background: #FFFFFF; box-shadow: none; border: 1px solid var(--gold-soft); }
        .bottom-nav-bar { border: 1px solid var(--border-subtle); box-shadow: 0 10px 30px rgba(27, 31, 42, 0.1); background: rgba(255, 255, 255, 0.94); border-radius: 999px; padding-left: 0.5rem; padding-right: 0.5rem; }
        .nav-tab { color: var(--text-muted); }
        .nav-tab-active { color: var(--accent) !important; }
        .nav-tab-active::after { display: block !important; width: 1rem; height: 2px; background: var(--gold); }
        .health-fill:not([class*="bg-"]) { background: var(--accent); }
        .health-track { box-shadow: none; background: #ECE8E1; height: 0.4rem; }
        .fab-primary { background: var(--accent); box-shadow: 0 8px 20px rgba(30, 42, 74, 0.28); }
        .pwa-install-card { box-shadow: none; background: #FFFFFF; border-radius: 1.25rem; }
        #app-login-screen { background: var(--bg-base); }
        .text-emerald-600, .text-emerald-700 { color: #17803D; }
        input, select, textarea { border-radius: 0.875rem; background: #FFFFFF; border: 1px solid var(--border-medium); }
        input:focus, select:focus, textarea:focus { box-shadow: 0 0 0 3px var(--gold-soft); border-color: var(--accent); outline: none; }
        :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; outline-color: var(--gold); }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
        }
"""

BODY_REPLACEMENTS = [
    ('class="w-full bg-white border border-slate-200 rounded-xl py-2 pl-3 pr-8 text-[11px] outline-none focus:ring-1 focus:ring-indigo-500"',
     'class="input-premium w-full rounded-xl py-2 pl-3 pr-8 text-[11px] outline-none"'),
    ('class="btn-primary flex-1 text-white text-[11px] font-bold py-2.5 px-3 transition-all flex items-center justify-center gap-1.5 active:scale-95"',
     'class="btn-primary flex-1 text-[11px] font-bold py-2.5 px-3 transition-all flex items-center justify-center gap-1.5 active:scale-95"'),
    ('class="btn-primary w-full text-white font-bold py-3 px-4 text-xs transition-all active:scale-95"',
     'class="btn-primary w-full font-bold py-3 px-4 text-xs transition-all active:scale-95"'),
]

SCRIPT_REPLACEMENTS = [
    ('<i class="fa-solid fa-gas-pump text-4xl text-[var(--accent)]/40 block"></i>',
     '<i class="fa-solid fa-gas-pump text-4xl text-[var(--accent)]/30 block"></i>'),
    ('<i class="fa-solid fa-wrench text-4xl text-[var(--accent)]/40 block"></i>',
     '<i class="fa-solid fa-wrench text-4xl text-[var(--accent)]/30 block"></i>'),
]


def apply_premium_html(text, replacements=None):
    replacements = BODY_REPLACEMENTS if replacements is None else replacements
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def apply_premium_script(text):
    return apply_premium_html(text, SCRIPT_REPLACEMENTS)

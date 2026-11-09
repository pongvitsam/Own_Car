"""Build static index.html for GitHub Pages from mockup + responsive GAS shell."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from seed_data import SEED_DATA, render_state_js  # noqa: E402
from premium_ui import PREMIUM_INLINE_STYLES, apply_premium_html, apply_premium_script  # noqa: E402
MOCKUP = os.path.join(ROOT, 'mockup', 'MyHome-CarCare-v1.8.html')
OUT = os.path.join(ROOT, 'index.html')

with open(MOCKUP, 'r', encoding='utf-8') as f:
    mockup = f.read()

script_matches = list(re.finditer(r'<script>(.*?)</script>', mockup, re.DOTALL))
script_match = max(script_matches, key=lambda m: len(m.group(1))) if script_matches else None
script = script_match.group(1) if script_match else ''

body_match = re.search(r'<body[^>]*>(.*?)(?=\s*<script>)', mockup, re.DOTALL)
body = body_match.group(1).strip() if body_match else ''

inline_styles = PREMIUM_INLINE_STYLES.strip()

# Version badge: single source of truth is package.json
import json
with open(os.path.join(ROOT, 'package.json'), 'r', encoding='utf-8-sig') as _pkg:
    APP_VERSION = json.load(_pkg)['version']
body = re.sub(
    r'(<span class="version-badge[^"]*"[^>]*>)(.*?)(</span>)',
    lambda m: m.group(1) + 'v' + APP_VERSION + m.group(3),
    body,
    count=1,
    flags=re.DOTALL
)

# Remove loading overlay (instant localStorage app) — match nested inner div
body = re.sub(
    r'\s*<div id="loading-overlay"[^>]*>[\s\S]*?</div>\s*</div>\s*',
    '',
    body,
    count=1,
)
# Clean any stray closing tag left by older builds
body = re.sub(r'^\s*</div>\s*\n', '', body, count=1)

# Search input: disable browser autocomplete (was suggesting "admin") — skip if GAS shell already patched
if 'autocomplete="off"' not in body and 'id="log-search-input"' in body:
    body = body.replace(
        'id="log-search-input" oninput="filterLogsList()"',
        'id="log-search-input" autocomplete="off" autocorrect="off" spellcheck="false" oninput="filterLogsList()"'
    )

# Year filter populated dynamically from maintenance logs per vehicle
body = re.sub(
    r'<select id="report-year-filter"[^>]*>.*?</select>',
    '<select id="report-year-filter" onchange="renderReportStats()" class="text-[11px] font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 rounded-xl px-2.5 py-1.5 outline-none focus:ring-2 focus:ring-indigo-500/40"></select>',
    body,
    count=1,
    flags=re.DOTALL
)


# --- Patch JavaScript for v2.0 GitHub Pages ---
script = script.replace(
    "localStorage.getItem('myhome_carcare_state_v1.7')",
    "localStorage.getItem('myhome_carcare_state_v2.2')"
)
script = script.replace(
    "localStorage.setItem('myhome_carcare_state_v1.7', JSON.stringify(state));",
    "localStorage.setItem('myhome_carcare_state_v2.2', JSON.stringify(state));"
)
script = script.replace(
    "localStorage.getItem('myhome_carcare_state_v2.0')",
    "localStorage.getItem('myhome_carcare_state_v2.2')"
)
script = script.replace(
    "localStorage.setItem('myhome_carcare_state_v2.0', JSON.stringify(state));",
    "localStorage.setItem('myhome_carcare_state_v2.2', JSON.stringify(state));"
)

script = script.replace(
    'let calendarSelectedDate = new Date(2026, 5, 6);',
    'let calendarSelectedDate = new Date();'
)
script = script.replace('let calendarViewMonth = 5;', 'let calendarViewMonth = new Date().getMonth();')
script = script.replace('let calendarViewYear = 2026;', 'let calendarViewYear = new Date().getFullYear();')

script = re.sub(
    r'function setDefaultDates\(\) \{[\s\S]*?\n        \}',
    """function setDefaultDates() {
            const now = new Date();
            const iso = toLocalIsoDate(now);
            setThaiDatePicker('rep-date', 'calendar-trigger-text', iso);
            setThaiDatePicker('fuel-date', 'fuel-calendar-trigger-text', iso);
            calendarSelectedDate = now;
            calendarViewMonth = now.getMonth();
            calendarViewYear = now.getFullYear();
        }""",
    script,
    count=1
)

script = script.replace(
    'setDefaultDates(); // Pre-populate default date (6 Jun 2026) immediately',
    'setDefaultDates();'
)

script = script.replace(
    'const isToday = day === 6 && calendarViewMonth === 5 && calendarViewYear === 2026;',
    """const today = new Date();
                const isToday = day === today.getDate() && calendarViewMonth === today.getMonth() && calendarViewYear === today.getFullYear();"""
)

for block in [
    """            calendarSelectedDate = new Date(2026, 5, 6);
            calendarViewMonth = 5; 
            calendarViewYear = 2026;
            syncCalendarDropdownSelectors();
            selectCalendarDate(6);""",
    """            syncCalendarDropdownSelectors();
            selectCalendarDate(6);""",
]:
    script = script.replace(
        block,
        """            calendarSelectedDate = new Date();
            calendarViewMonth = calendarSelectedDate.getMonth();
            calendarViewYear = calendarSelectedDate.getFullYear();
            syncCalendarDropdownSelectors();
            selectCalendarDate(calendarSelectedDate.getDate());"""
    )

# Debounced search
if 'searchDebounceTimer' not in script:
    script = script.replace(
        'let currentUploadedReceiptBase64 = "";',
        'let currentUploadedReceiptBase64 = "";\n        let searchDebounceTimer = null;'
    )
    script = re.sub(
        r'// Search Filter for History\s*\n\s*function filterLogsList\(\) \{[\s\S]*?\n        \}',
        """// Search Filter for History (debounced 300ms)
        function filterLogsList() {
            clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(filterLogsListNow, 300);
        }

        function filterLogsListNow() {
            const val = document.getElementById('log-search-input').value;
            const clearBtn = document.getElementById('clear-search-btn');
            if (val.trim() !== '') {
                clearBtn.classList.remove('hidden');
            } else {
                clearBtn.classList.add('hidden');
            }
            renderLogsHistory(state.selectedVehicleId, val);
        }""",
        script,
        count=1
    )

# Client-side PDF export (print window) — fallback if mockup lacks exportReportPdf
EXPORT_FN = '''
        function formatPdfNextCycleFromLog(log) {
            if (!log || log.type !== 'Maintenance' || (!log.alertKm && !log.alertMonth)) {
                return '—';
            }
            const cat = state.categories.find(c => c.id === log.category);
            const label = cat ? cat.name : 'บำรุงรักษาตามกำหนด';
            const bits = [label];
            if (log.alertKm > 0) {
                bits.push('ตรวจระยะรอบต่อไป: ' + (log.odo + log.alertKm).toLocaleString() + ' กม.');
            }
            if (log.alertMonth > 0) {
                const d = new Date(log.date);
                d.setMonth(d.getMonth() + log.alertMonth);
                const y = d.getFullYear();
                const m = String(d.getMonth() + 1).padStart(2, '0');
                const day = String(d.getDate()).padStart(2, '0');
                bits.push(y + '-' + m + '-' + day);
            }
            return bits.join(' — ');
        }

        function formatPdfActiveNextCycleHtml(vehicleId) {
            const alertObj = state.alerts.find(a => a.vehicleId === vehicleId && a.status === 'Active');
            if (!alertObj) {
                return '<p style="color:#94a3b8">ยังไม่ได้รับการตั้งการเตือน</p>';
            }
            const serviceLabel = resolveAlertServiceLabel(alertObj);
            let html = '<p>รายการถัดไป: <strong>' + serviceLabel + '</strong></p>';
            html += '<p>ตรวจระยะรอบต่อไป: <strong>' + alertObj.targetKm.toLocaleString() + ' กม.</strong>';
            if (alertObj.targetDate) {
                html += ' / ' + alertObj.targetDate;
            }
            html += '</p>';
            return html;
        }

        function exportReportPdf() {
            const year = document.getElementById('report-year-filter').value;
            const vehicleId = state.selectedVehicleId;
            if (!vehicleId) {
                showToast('กรุณาเลือกรถก่อนส่งออกรายงาน', 'error');
                return;
            }
            const vehicle = state.vehicles.find(v => v.id === vehicleId);
            if (!vehicle) {
                showToast('ไม่พบรถ', 'error');
                return;
            }
            const logs = state.maintenanceLogs.filter(l => {
                if (l.type !== 'Maintenance' || l.vehicleId !== vehicleId) return false;
                const logYear = getLogYear(l.date);
                return logYear !== null && String(logYear) === String(year);
            });
            const total = logs.reduce((sum, l) => sum + l.cost, 0);
            const categorySums = {};
            logs.forEach(l => {
                const cat = state.categories.find(c => c.id === l.category);
                const name = cat ? cat.name : 'อื่นๆ';
                categorySums[name] = (categorySums[name] || 0) + l.cost;
            });
            const buddhistYear = parseInt(year, 10) + 543;
            const fmtNum = n => Number(n || 0).toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');
            const fmtMoney = n => Number(n || 0).toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');
            const rows = logs.map(l =>
                '<tr><td>' + l.date + '</td><td>' + l.shop + '</td><td>' + fmtNum(l.odo) +
                '</td><td>' + formatPdfNextCycleFromLog(l) +
                '</td><td style="text-align:right">฿' + l.cost.toFixed(2) + '</td></tr>'
            ).join('');
            const catList = Object.keys(categorySums).map(name => {
                const sum = categorySums[name];
                const pct = total > 0 ? ((sum / total) * 100).toFixed(0) : 0;
                return '<li>' + name + ': ฿' + fmtNum(sum) + ' (' + pct + '%)</li>';
            }).join('');
            const html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>รายงาน ' + vehicle.license + '</title>' +
                '<style>body{font-family:Sarabun,Inter,Arial,sans-serif;padding:24px;color:#1e293b}' +
                'h1{font-size:20px;margin-bottom:4px}table{width:100%;border-collapse:collapse;margin-top:16px}' +
                'th,td{border:1px solid #cbd5e1;padding:8px;font-size:12px}th{background:#eef2ff}' +
                '.summary{background:#f8fafc;padding:12px;border-radius:8px;margin-top:12px}' +
                '@media print{body{padding:12px}}</style></head><body>' +
                '<h1>MyHome CarCare - รายงานค่าบำรุงรักษา</h1>' +
                '<p>รถ: <strong>' + vehicle.name + '</strong> (' + vehicle.license + ')</p>' +
                '<p>ปี พ.ศ. ' + buddhistYear + ' (ค.ศ. ' + year + ')</p>' +
                '<div class="summary"><p>ยอดรวม: <strong>฿' + fmtMoney(total) + '</strong></p>' +
                '<p>จำนวนรายการ: ' + logs.length + '</p><ul>' + catList + '</ul>' +
                formatPdfActiveNextCycleHtml(vehicleId) + '</div>' +
                '<table><thead><tr><th>วันที่</th><th>ร้าน/ศูนย์</th><th>ไมล์</th><th>ระยะรอบต่อไป</th><th>ค่าใช้จ่าย</th></tr></thead><tbody>' +
                (rows || '<tr><td colspan="5">ไม่มีข้อมูลในปีนี้</td></tr>') + '</tbody></table>' +
                '<p style="font-size:10px;color:#64748b;margin-top:24px">MyHome CarCare v2.0.0 GitHub Pages — ' +
                new Date().toLocaleString('th-TH', { timeZone: 'Asia/Bangkok' }) + '</p></body></html>';
            const w = window.open('', '_blank');
            if (!w) {
                showToast('โปรดอนุญาต Pop-up เพื่อส่งออก PDF', 'warning');
                return;
            }
            w.document.write(html);
            w.document.close();
            w.focus();
            setTimeout(function() { w.print(); }, 400);
            showToast('เปิดหน้าต่างพิมพ์/บันทึก PDF แล้ว');
        }
'''


# Ensure setupDailyTrigger exists for GitHub Pages (simulation)
SETUP_TRIGGER_FN = '''
        function setupDailyTrigger() {
            const statusEl = document.getElementById('setup-trigger-status');
            const ts = new Date().toLocaleString('th-TH', { timeZone: 'Asia/Bangkok' });
            state.lineLogs.push(`⏰ [${ts}] จำลองสร้าง Daily Trigger 08:00 น. สำเร็จ (GitHub Pages — ไม่มี Apps Script จริง)`);
            saveToLocalStorage();
            if (statusEl) {
                statusEl.textContent = '✓ จำลองสร้าง trigger สำเร็จ — ใน GAS จริงจะรันที่ Apps Script';
                statusEl.classList.remove('hidden');
            }
            showToast('จำลองสร้าง Daily Trigger 08:00 น. สำเร็จ (GitHub Pages)');
        }
'''

# Fix search matching "admin" inside "Maintenance" type string
script = script.replace(
    """                    const typeMatch = l.type.toLowerCase().includes(kw);
                    return shopMatch || catMatch || typeMatch;""",
    """                    const odoMatch = String(l.odo).includes(kw);
                    return shopMatch || catMatch || odoMatch;"""
)
script = script.replace(
    'const shopMatch = l.shop.toLowerCase().includes(kw);',
    "const shopMatch = (l.shop || '').toLowerCase().includes(kw);"
)



# Vehicle admin edit (ชื่อรถ + ทะเบียน) — mockup is source; verify after other patches
if 'function saveVehicleEditAdmin' not in script:
    raise SystemExit(
        'FAIL: mockup must define saveVehicleEditAdmin / vehicle edit UI before build'
    )

# Truncate long names in admin lists (legacy mockups without gap-2)
script = script.replace(
    """                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                        <div>
                            <span class="font-extrabold text-slate-800 text-xs">${v.name}</span>
                            <span class="text-[9px] text-slate-500 block font-bold font-mono">${v.license}</span>
                        </div>
                        <button onclick="deleteVehicleAdmin('${v.id}')" class="text-rose-500 hover:text-rose-700 p-1">""",
    """                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-lg border border-slate-200 gap-2">
                        <div class="min-w-0 flex-1">
                            <span class="font-extrabold text-slate-800 text-xs block truncate" title="${v.name}">${v.name}</span>
                            <span class="text-[9px] text-slate-500 block font-bold font-mono truncate">${v.license}</span>
                        </div>
                        <button onclick="deleteVehicleAdmin('${v.id}')" class="text-rose-500 hover:text-rose-700 p-1 shrink-0">"""
)
script = script.replace(
    """                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                        <span class="font-extrabold text-slate-800 text-xs">${c.name}</span>
                        <button onclick="deleteCategoryAdmin('${c.id}')" class="text-rose-500 hover:text-rose-700 p-1">""",
    """                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-lg border border-slate-200 gap-2">
                        <span class="font-extrabold text-slate-800 text-xs truncate min-w-0 flex-1" title="${c.name}">${c.name}</span>
                        <button onclick="deleteCategoryAdmin('${c.id}')" class="text-rose-500 hover:text-rose-700 p-1 shrink-0">"""
)

script = re.sub(
    r"function logoutAdmin\(\) \{[\s\S]*?showToast\(\"ออกจากระบบแอดมินเรียบร้อย\"\);\s*\n        \}",
    """function logoutAdmin() {
            state.adminAuthenticated = false;
            document.getElementById('admin-username').value = '';
            document.getElementById('admin-passcode').value = '';
            renderAdminPanelState();
            showToast("ออกจากระบบแอดมินเรียบร้อย");
        }""",
    script,
    count=1
)

# Footer nav active indicator (light Sarabun nav-tab classes)
script = script.replace(
    """            tabs.forEach(t => {
                const navBtn = document.getElementById(`nav-${t}`);
                if (t === tabId) {
                    navBtn.className = "flex flex-col items-center justify-center w-16 text-indigo-600 transition-all font-bold";
                } else {
                    navBtn.className = "flex flex-col items-center justify-center w-16 text-slate-400 transition-all";
                }
            });""",
    """            tabs.forEach(t => {
                const navBtn = document.getElementById(`nav-${t}`);
                if (t === tabId) {
                    navBtn.className = "nav-tab nav-tab-active flex flex-col items-center justify-center w-16 transition-all";
                } else {
                    navBtn.className = "nav-tab flex flex-col items-center justify-center w-16 text-[var(--text-muted)] hover:text-[var(--accent)] transition-all";
                }
            });"""
)

body = apply_premium_html(body)
script = apply_premium_script(script)



script = script.replace(
    """                const alertObj = state.alerts.find(a => a.vehicleId === id && a.status === 'Active');
                const targetKmSpan = document.getElementById('target-odometer-val');
                const targetTimeSpan = document.getElementById('target-time-val');
                const statusBadge = document.getElementById('vehicle-status-badge');

                if (alertObj) {
                    targetKmSpan.innerHTML = `ตรวจระยะรอบต่อไป: <span class="text-indigo-700 font-extrabold">${alertObj.targetKm.toLocaleString()} กม.</span>`;
                    targetTimeSpan.innerHTML = `<i class="fa-solid fa-clock"></i> เตือนล่วงหน้า: ${formatThaiDate(alertObj.targetDate)}`;""",
    """                const alertObj = state.alerts.find(a => a.vehicleId === id && a.status === 'Active');
                const targetServiceSpan = document.getElementById('target-service-val');
                const targetKmSpan = document.getElementById('target-odometer-val');
                const targetTimeSpan = document.getElementById('target-time-val');
                const statusBadge = document.getElementById('vehicle-status-badge');

                if (alertObj) {
                    const serviceLabel = resolveAlertServiceLabel(alertObj);
                    if (targetServiceSpan) {
                        targetServiceSpan.innerHTML = `รายการถัดไป: <span class="font-extrabold">${serviceLabel}</span>`;
                    }
                    targetKmSpan.innerHTML = `ตรวจระยะรอบต่อไป: <span class="text-indigo-700 font-extrabold">${alertObj.targetKm.toLocaleString()} กม.</span>`;
                    targetTimeSpan.innerHTML = `<i class="fa-solid fa-clock"></i> เตือนล่วงหน้า: ${formatThaiDate(alertObj.targetDate)}`;""",
    1,
)

script = script.replace(
    """                } else {
                    targetKmSpan.innerHTML = `<span class="text-slate-400">ยังไม่ได้รับการตั้งการเตือน</span>`;
                    targetTimeSpan.innerHTML = `<i class="fa-solid fa-circle-info"></i> ปลอดภัย`;""",
    """                } else {
                    if (targetServiceSpan) targetServiceSpan.innerHTML = '';
                    targetKmSpan.innerHTML = `<span class="text-slate-400">ยังไม่ได้รับการตั้งการเตือน</span>`;
                    targetTimeSpan.innerHTML = `<i class="fa-solid fa-circle-info"></i> ปลอดภัย`;""",
    1,
)

script = script.replace(
    """                state.alerts = state.alerts.filter(a => a.vehicleId !== vId);
                state.alerts.push({
                    vehicleId: vId,
                    targetKm: targetKm,
                    targetDate: targetDateStr,
                    status: 'Active',
                    lastUpdated: repairDate
                });

                state.lineLogs.push(`⏰ [${new Date().toLocaleTimeString()}] ตั้งค่ารอบตรวจสอบของคัน ${vId}: เป้าหมาย ${targetKm.toLocaleString()} กม. หรือ ${targetDateStr}`);""",
    """                const catObj = state.categories.find(c => c.id === category);
                const serviceLabel = catObj ? catObj.name : 'บำรุงรักษาตามกำหนด';

                state.alerts = state.alerts.filter(a => a.vehicleId !== vId);
                state.alerts.push({
                    vehicleId: vId,
                    targetKm: targetKm,
                    targetDate: targetDateStr,
                    status: 'Active',
                    lastUpdated: repairDate,
                    serviceLabel: serviceLabel,
                    categoryId: category
                });

                state.lineLogs.push(`⏰ [${new Date().toLocaleTimeString()}] ตั้งค่ารอบตรวจสอบของคัน ${vId}: ${serviceLabel} — เป้าหมาย ${targetKm.toLocaleString()} กม. หรือ ${targetDateStr}`);""",
    1,
)

# Real vehicle seed data (Mazda, Click 160, Altis)
script = re.sub(
    r'let state = \{[\s\S]*?\n        \};',
    render_state_js(),
    script,
    count=1,
)

AUTH_BOOT_SCRIPT = (
    "<script>try{if(localStorage.getItem('myhome_carcare_device_login_v1')==='ok')"
    "document.documentElement.classList.add('carcare-authed')}catch(e){}</script>"
)

index_html = f'''<!DOCTYPE html>
<html lang="th" class="h-full min-h-full bg-[#F7F8FA]">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#1E2A4A">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="CarCare">
    <meta name="description" content="บำรุงรักษารถครอบครัวและบันทึกน้ำมันสไตล์ Fuelio">
    <link rel="manifest" href="./manifest.webmanifest">
    <link rel="icon" href="./icons/icon-192.png" type="image/png">
    <link rel="apple-touch-icon" href="./icons/icon-180.png">
    <title>MyHome CarCare - ระบบบำรุงรักษาและบันทึกน้ำมันสไตล์ Fuelio</title>
    {AUTH_BOOT_SCRIPT}
    <link rel="stylesheet" href="./assets/tailwind.min.css">
    <link rel="stylesheet" href="./assets/fa-subset.css">
    <style>
{inline_styles}
    </style>
</head>
<body class="min-h-dvh bg-[var(--bg-base)]">
{body}
    <script>
/*__APP_JS_BEGIN__*/{script}/*__APP_JS_END__*/
    </script>
</body>
</html>
'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(index_html)

def compile_tailwind():
    import subprocess
    assets_dir = os.path.join(ROOT, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    out_css = os.path.join(assets_dir, 'tailwind.min.css')
    subprocess.run(
        ['npx', '--yes', 'tailwindcss@3.4.17',
         '-c', 'tools/tailwind.config.js',
         '-i', 'tools/tailwind.input.css',
         '-o', 'assets/tailwind.min.css',
         '--minify'],
        cwd=ROOT, check=True, shell=(os.name == 'nt'),
    )
    if not os.path.isfile(out_css) or os.path.getsize(out_css) < 500:
        raise RuntimeError('compiled CSS missing or too small')
    print(f'Compiled {out_css} ({os.path.getsize(out_css):,} bytes)')
    return out_css

APP_JS_BEGIN = '/*__APP_JS_BEGIN__*/'
APP_JS_END = '/*__APP_JS_END__*/'
TERSER_SPEC = 'terser@5.36.0'

def minify_js(source):
    import subprocess
    src_path = os.path.join(ROOT, 'tools', '_app.tmp.js')
    out_path = os.path.join(ROOT, 'tools', '_app.min.js')
    try:
        with open(src_path, 'w', encoding='utf-8') as tmp:
            tmp.write(source)
        subprocess.run(
            ['npx', '--yes', TERSER_SPEC, 'tools/_app.tmp.js',
             '--compress', 'unused=false,dead_code=false',
             '--comments', 'false',
             '--output', 'tools/_app.min.js'],
            cwd=ROOT, check=True, shell=(os.name == 'nt'),
        )
        with open(out_path, 'r', encoding='utf-8') as tmp:
            minified = tmp.read()
        if len(minified) < 1000:
            raise RuntimeError('terser output too small')
        print(f'Minified JS {len(source):,} -> {len(minified):,} chars')
        return minified
    finally:
        for path in (src_path, out_path):
            try:
                os.remove(path)
            except OSError:
                pass

def inline_css_and_minify_js(html, css_path):
    with open(css_path, 'r', encoding='utf-8') as css_file:
        tw_css = css_file.read().strip()
    link = '<link rel="stylesheet" href="./assets/tailwind.min.css">'
    if link not in html:
        raise RuntimeError('tailwind stylesheet link not found in template')
    html = html.replace(link, f'<style>{tw_css}</style>', 1)
    start = html.find(APP_JS_BEGIN)
    end = html.find(APP_JS_END)
    if start < 0 or end < start:
        raise RuntimeError('app script markers not found')
    inner = html[start + len(APP_JS_BEGIN):end]
    return html[:start] + minify_js(inner) + html[end + len(APP_JS_END):]

# Any failure here aborts the build: shipping the CDN fallback or an unminified
# page would silently break offline use.
css_file = compile_tailwind()
index_html = inline_css_and_minify_js(index_html, css_file)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(index_html)

# Stamp the service-worker cache name with a content hash so every rebuilt
# index.html invalidates old caches without a manual version bump.
import hashlib
SW_PATH = os.path.join(ROOT, 'sw.js')
with open(SW_PATH, 'r', encoding='utf-8') as f:
    sw_src = f.read()
digest = hashlib.sha256(index_html.encode('utf-8')).hexdigest()[:10]
sw_src, n_sub = re.subn(r"const CACHE = '[^']*';", f"const CACHE = 'carcare-{digest}';", sw_src, count=1)
if n_sub != 1:
    raise SystemExit('FAIL: CACHE constant not found in sw.js')
with open(SW_PATH, 'w', encoding='utf-8') as f:
    f.write(sw_src)

# Verify no raw CSS outside style tags
raw_css_pattern = re.compile(r'body\s*\{\s*font-family', re.IGNORECASE)
outside_style = []
for i, line in enumerate(index_html.splitlines(), 1):
    if raw_css_pattern.search(line) and '<style>' not in line and '</style>' not in line:
        # Check if we're inside a style block (simple heuristic)
        before = index_html[:index_html.find(line)]
        if before.count('<style>') <= before.count('</style>'):
            outside_style.append(i)

if outside_style:
    raise SystemExit(f'FAIL: Raw CSS outside <style> at lines: {outside_style}')

if '<?!=' in index_html or "include('Styles')" in index_html or "include('Scripts')" in index_html:
    raise SystemExit('FAIL: GAS template includes found in index.html')

print(f'Generated {OUT} OK ({len(index_html):,} bytes)')
print('Verified: all CSS inside <style> tags, no GAS includes')

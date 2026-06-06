"""Build static index.html for GitHub Pages from mockup + responsive GAS shell."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from seed_data import SEED_DATA, render_state_js  # noqa: E402
MOCKUP = os.path.join(ROOT, 'mockup', 'MyHome-CarCare-v1.8.html')
GAS_INDEX = os.path.join(ROOT, 'gas', 'Index.html')
OUT = os.path.join(ROOT, 'index.html')

with open(MOCKUP, 'r', encoding='utf-8') as f:
    mockup = f.read()

with open(GAS_INDEX, 'r', encoding='utf-8') as f:
    gas_index = f.read()

script_match = re.search(r'<script>(.*?)</script>', mockup, re.DOTALL)
script = script_match.group(1) if script_match else ''

body_match = re.search(
    r'<body[^>]*>(.*?)<\?!= include\(\'Scripts\'\); \?>',
    gas_index,
    re.DOTALL
)
if not body_match:
    body_match = re.search(r'<body[^>]*>(.*?)</body>', gas_index, re.DOTALL)
body = body_match.group(1).strip() if body_match else ''

style_match = re.search(r'<style>(.*?)</style>', gas_index, re.DOTALL)
inline_styles = style_match.group(1).strip() if style_match else ''

# Version badge (GitHub Pages) — inject GitHub icon if shell already has version-badge
body = re.sub(
    r'(<span class="version-badge[^"]*"[^>]*>)(?!.*fa-github)(.*?)(</span>)',
    r'\1<i class="fa-brands fa-github text-[8px] opacity-80"></i> v2.1.0 Premium\3',
    body,
    count=1,
    flags=re.DOTALL
)
body = re.sub(
    r'<span class="version-badge">.*?</span>',
    '<span class="version-badge text-[9px] text-indigo-100 font-mono"><i class="fa-brands fa-github text-[8px] opacity-80"></i> v2.1.0 Premium</span>',
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

# Per-vehicle annual stats: reset year dropdown when carousel vehicle changes
if 'reportYearFilterVehicleId' not in script:
    script = script.replace(
        'let searchDebounceTimer = null;',
        'let searchDebounceTimer = null;\n        let reportYearFilterVehicleId = null;'
    )
    script = script.replace(
        "const activeTab = document.querySelector('.tab-content:not(.hidden)').id;",
        "const activeTabEl = document.querySelector('.tab-content:not(.hidden)');\n"
        "            const activeTab = activeTabEl ? activeTabEl.id : '';"
    )
    script = script.replace(
        """                calculateVehicleMetrics(id);
                renderLogsHistory(id);
                renderReports();
            } else if (activeTab === 'tab-fuelio') {
                renderFuelLogs();
            }
        }""",
        """                calculateVehicleMetrics(id);
                clearLogSearch();
                refreshVehicleAnnualReport(id);
                renderLogsHistory(id);
            } else if (activeTab === 'tab-fuelio') {
                reportYearFilterVehicleId = null;
                renderFuelLogs();
            } else {
                reportYearFilterVehicleId = null;
            }
        }

        function clearLogSearch() {
            const searchInput = document.getElementById('log-search-input');
            const clearBtn = document.getElementById('clear-search-btn');
            if (searchInput) searchInput.value = '';
            if (clearBtn) clearBtn.classList.add('hidden');
        }"""
    )
    script = script.replace(
        'function populateReportYearFilter(vehicleId) {',
        'function populateReportYearFilter(vehicleId, resetYear) {'
    )
    script = script.replace(
        """            const previousValue = yearFilterEl.value;
            yearFilterEl.innerHTML = years.map(y =>
                `<option value="${y}">พ.ศ. ${y + 543}</option>`
            ).join('');

            const currentYear = new Date().getFullYear();
            let selectedYear;
            if (previousValue && years.includes(parseInt(previousValue, 10))) {
                selectedYear = parseInt(previousValue, 10);
            } else if (yearCounts[currentYear]) {
                selectedYear = currentYear;
            } else {
                selectedYear = years.reduce((best, y) =>
                    (yearCounts[y] > (yearCounts[best] || 0)) ? y : best, years[0]);
            }
            yearFilterEl.value = String(selectedYear);
            return selectedYear;
        }

        // Render Reports (Annual spending visualization inside tab 1)
        function renderReports() {
            const yearFilterEl = document.getElementById('report-year-filter');
            if (!yearFilterEl) return;

            const targetVehicle = state.selectedVehicleId;
            if (!targetVehicle) return;

            populateReportYearFilter(targetVehicle);
            const targetYear = yearFilterEl.value;

            const yearLogs = state.maintenanceLogs.filter(l => {""",
        """            const preserveYear = !resetYear && reportYearFilterVehicleId === vehicleId;
            const previousValue = preserveYear ? yearFilterEl.value : null;
            yearFilterEl.innerHTML = years.map(y =>
                `<option value="${y}">พ.ศ. ${y + 543}</option>`
            ).join('');

            const currentYear = new Date().getFullYear();
            let selectedYear;
            const prev = previousValue != null ? parseInt(previousValue, 10) : NaN;
            if (!Number.isNaN(prev) && years.includes(prev)) {
                selectedYear = prev;
            } else if (yearCounts[currentYear]) {
                selectedYear = currentYear;
            } else {
                selectedYear = years.reduce((best, y) =>
                    (yearCounts[y] > (yearCounts[best] || 0)) ? y : best, years[0]);
            }
            yearFilterEl.value = String(selectedYear);
            reportYearFilterVehicleId = vehicleId;
            return selectedYear;
        }

        function refreshVehicleAnnualReport(vehicleId) {
            populateReportYearFilter(vehicleId, true);
            renderReportStats();
        }

        function renderReportStats() {
            const yearFilterEl = document.getElementById('report-year-filter');
            if (!yearFilterEl) return;

            const targetVehicle = state.selectedVehicleId;
            if (!targetVehicle) return;

            const targetYear = yearFilterEl.value;

            const yearLogs = state.maintenanceLogs.filter(l => {"""
    )
    script = script.replace(
        """            if (total === 0) {
                barContainer.innerHTML = `
                    <div class="text-center py-6 text-slate-400 text-[10px] font-bold bg-slate-50 border border-slate-200 border-dashed rounded-xl">
                        ไม่พบประวัติการใช้จ่ายในปี พ.ศ. ${parseInt(targetYear) + 543} ของรถคันนี้
                    </div>
                `;
            }
        }

        // ADMIN TAB STATE MANAGEMENT""",
        """            if (total === 0) {
                barContainer.innerHTML = `
                    <div class="text-center py-6 text-slate-400 text-[10px] font-bold bg-slate-50 border border-slate-200 border-dashed rounded-xl">
                        ไม่พบประวัติการใช้จ่ายในปี พ.ศ. ${parseInt(targetYear) + 543} ของรถคันนี้
                    </div>
                `;
            }
        }

        function renderReports() {
            const targetVehicle = state.selectedVehicleId;
            if (!targetVehicle) return;
            populateReportYearFilter(targetVehicle, false);
            renderReportStats();
        }

        // ADMIN TAB STATE MANAGEMENT"""
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
    'let calendarSelectedDate = new Date(2026, 5, 6); // Default 6 June 2026',
    'let calendarSelectedDate = new Date();'
)
script = script.replace('let calendarViewMonth = 5;', 'let calendarViewMonth = new Date().getMonth();')
script = script.replace('let calendarViewYear = 2026;', 'let calendarViewYear = new Date().getFullYear();')

script = re.sub(
    r'function setDefaultDates\(\) \{[\s\S]*?\n        \}',
    """function setDefaultDates() {
            const now = new Date();
            const iso = now.toISOString().split('T')[0];
            const thaiStr = formatThaiDate(iso);
            const repDate = document.getElementById('rep-date');
            const calText = document.getElementById('calendar-trigger-text');
            const fuelDate = document.getElementById('fuel-date');
            const fuelCalText = document.getElementById('fuel-calendar-trigger-text');
            if (repDate) repDate.value = iso;
            if (calText) calText.textContent = thaiStr;
            if (fuelDate) fuelDate.value = iso;
            if (fuelCalText) fuelCalText.textContent = thaiStr;
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

# Client-side PDF export (print window)
EXPORT_FN = '''
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
                '</td><td style="text-align:right">฿' + l.cost.toFixed(2) + '</td></tr>'
            ).join('');
            const catList = Object.keys(categorySums).map(name => {
                const sum = categorySums[name];
                const pct = total > 0 ? ((sum / total) * 100).toFixed(0) : 0;
                return '<li>' + name + ': ฿' + fmtNum(sum) + ' (' + pct + '%)</li>';
            }).join('');
            const html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>รายงาน ' + vehicle.license + '</title>' +
                '<style>body{font-family:Itim,Inter,Arial,sans-serif;padding:24px;color:#1e293b}' +
                'h1{font-size:20px;margin-bottom:4px}table{width:100%;border-collapse:collapse;margin-top:16px}' +
                'th,td{border:1px solid #cbd5e1;padding:8px;font-size:12px}th{background:#eef2ff}' +
                '.summary{background:#f8fafc;padding:12px;border-radius:8px;margin-top:12px}' +
                '@media print{body{padding:12px}}</style></head><body>' +
                '<h1>MyHome CarCare - รายงานค่าบำรุงรักษา</h1>' +
                '<p>รถ: <strong>' + vehicle.name + '</strong> (' + vehicle.license + ')</p>' +
                '<p>ปี พ.ศ. ' + buddhistYear + ' (ค.ศ. ' + year + ')</p>' +
                '<div class="summary"><p>ยอดรวม: <strong>฿' + fmtMoney(total) + '</strong></p>' +
                '<p>จำนวนรายการ: ' + logs.length + '</p><ul>' + catList + '</ul></div>' +
                '<table><thead><tr><th>วันที่</th><th>ร้าน/ศูนย์</th><th>ไมล์</th><th>ค่าใช้จ่าย</th></tr></thead><tbody>' +
                (rows || '<tr><td colspan="4">ไม่มีข้อมูลในปีนี้</td></tr>') + '</tbody></table>' +
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

if 'function exportReportPdf' not in script:
    script = script.replace(
        'window.onload = function () {',
        EXPORT_FN + '\n        window.onload = function () {'
    )

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
if 'function setupDailyTrigger' not in script:
    script = script.replace(
        '        // Tab routing helper',
        SETUP_TRIGGER_FN + '\n        // Tab routing helper',
        1
    )

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

# Admin login: username + password (admin / 1234)
if 'id="admin-username"' not in body:
    body = body.replace(
        """                    <p class="text-[10px] text-slate-500">กรุณากรอกรหัสผ่านเพื่อแก้ไขชื่อและประเภทรถในครอบครัว</p>""",
        """                    <p class="text-[10px] text-slate-500">กรุณากรอกชื่อผู้ใช้และรหัสผ่านเพื่อแก้ไขชื่อและประเภทรถในครอบครัว</p>"""
    )
    body = body.replace(
        """                    <input type="password" id="admin-passcode" name="carcare-admin-pass" autocomplete="new-password" placeholder="ใส่รหัสผ่านเข้าสู่ระบบ (เริ่มต้น: 1234)" class="w-full text-center bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500">
                    <button onclick="authenticateAdmin()" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl text-xs transition-all active:scale-95 shadow-md">
                        ยืนยันรหัสผ่านเพื่อเข้าใช้งาน
                    </button>""",
        """                    <input type="text" id="admin-username" name="carcare-admin-user" autocomplete="username" placeholder="ชื่อผู้ใช้ (เริ่มต้น: admin)" class="w-full text-center bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500">
                    <input type="password" id="admin-passcode" name="carcare-admin-pass" autocomplete="current-password" placeholder="รหัสผ่าน (เริ่มต้น: 1234)" class="w-full text-center bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500">
                    <button onclick="authenticateAdmin()" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl text-xs transition-all active:scale-95 shadow-md">
                        เข้าสู่ระบบแอดมิน
                    </button>"""
    )
    body = body.replace(
        """                        <li>รหัสแอดมินเริ่มต้น: <strong>1234</strong></li>""",
        """                        <li>บัญชีแอดมินเริ่มต้น: <strong>admin</strong> / รหัสผ่าน <strong>1234</strong></li>"""
    )

if "user === 'admin' && pass === '1234'" not in script:
    script = script.replace(
        """        function authenticateAdmin() {
            const pass = document.getElementById('admin-passcode').value;
            if (pass === '1234') {
                state.adminAuthenticated = true;
                showToast("ยินดีต้อนรับแอดมินบ้าน เข้าสู่โหมดควบคุมแล้ว");
                renderAdminPanelState();
            } else {
                showToast("รหัสผ่านไม่ถูกต้อง! ลองใส่ 1234", "error");
            }
        }""",
        """        function authenticateAdmin() {
            const user = document.getElementById('admin-username').value.trim();
            const pass = document.getElementById('admin-passcode').value;
            if (user === 'admin' && pass === '1234') {
                state.adminAuthenticated = true;
                showToast("ยินดีต้อนรับแอดมินบ้าน เข้าสู่โหมดควบคุมแล้ว");
                renderAdminPanelState();
            } else {
                showToast("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง! (admin / 1234)", "error");
            }
        }"""
    )
    script = script.replace(
        """        function logoutAdmin() {
            state.adminAuthenticated = false;
            document.getElementById('admin-passcode').value = '';
            renderAdminPanelState();
            showToast("ออกจากระบบแอดมินเรียบร้อย");
        }""",
        """        function logoutAdmin() {
            state.adminAuthenticated = false;
            document.getElementById('admin-username').value = '';
            document.getElementById('admin-passcode').value = '';
            renderAdminPanelState();
            showToast("ออกจากระบบแอดมินเรียบร้อย");
        }"""
    )
    script = script.replace(
        '// ADMIN TAB STATE MANAGEMENT (Rule: แผงแอดมินรหัส 1234)',
        '// ADMIN TAB STATE MANAGEMENT (Rule: แผงแอดมิน admin / 1234)'
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

# Admin login: username admin + password 1234
if 'admin-username' not in body:
    body = body.replace(
        '<p class="text-[10px] text-slate-500">กรุณากรอกรหัสผ่านเพื่อแก้ไขชื่อและประเภทรถในครอบครัว</p>',
        '<p class="text-[10px] text-slate-500">กรุณากรอกชื่อผู้ใช้และรหัสผ่านเพื่อแก้ไขชื่อและประเภทรถในครอบครัว</p>'
    )
    body = body.replace(
        '<input type="password" id="admin-passcode" name="carcare-admin-pass" autocomplete="new-password" placeholder="ใส่รหัสผ่านเข้าสู่ระบบ (เริ่มต้น: 1234)" class="w-full text-center bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500">',
        '<input type="text" id="admin-username" name="carcare-admin-user" autocomplete="username" placeholder="ชื่อผู้ใช้ (เริ่มต้น: admin)" class="w-full text-center bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500">\n'
        '                    <input type="password" id="admin-passcode" name="carcare-admin-pass" autocomplete="current-password" placeholder="รหัสผ่าน (เริ่มต้น: 1234)" class="w-full text-center bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500">'
    )
    body = body.replace(
        'ยืนยันรหัสผ่านเพื่อเข้าใช้งาน',
        'เข้าสู่ระบบแอดมิน'
    )
body = body.replace(
    'รหัสแอดมินเริ่มต้น: <strong>1234</strong>',
    'บัญชีแอดมินเริ่มต้น: <strong>admin</strong> / รหัสผ่าน <strong>1234</strong>'
)

script = re.sub(
    r'function authenticateAdmin\(\) \{[\s\S]*?\n        \}',
    """function authenticateAdmin() {
            const user = document.getElementById('admin-username').value.trim();
            const pass = document.getElementById('admin-passcode').value;
            if (user === 'admin' && pass === '1234') {
                state.adminAuthenticated = true;
                showToast("ยินดีต้อนรับแอดมินบ้าน เข้าสู่โหมดควบคุมแล้ว");
                renderAdminPanelState();
            } else {
                showToast("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง! (admin / 1234)", "error");
            }
        }""",
    script,
    count=1
)
script = script.replace(
    '// ADMIN TAB STATE MANAGEMENT (Rule: แผงแอดมินรหัส 1234)',
    '// ADMIN TAB STATE MANAGEMENT (Rule: แผงแอดมิน admin / 1234)'
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

# Footer nav active indicator
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
                    navBtn.className = "nav-tab nav-tab-active flex flex-col items-center justify-center w-16 text-indigo-600 transition-all";
                } else {
                    navBtn.className = "nav-tab flex flex-col items-center justify-center w-16 text-slate-400 hover:text-indigo-400 transition-all";
                }
            });"""
)

# Itim typography + UI polish in inline CSS (skip if GAS shell already uses Itim)
if "'Itim'" not in inline_styles:
    inline_styles = inline_styles.replace(
        "font-family: 'Inter', 'Sarabun', sans-serif;",
        "font-family: 'Itim', 'Inter', sans-serif;"
    )
if '--radius-sm' not in inline_styles and '.nav-tab-active::after' not in inline_styles:
    inline_styles += """
        .nav-tab { position: relative; min-height: 3rem; }
        .nav-tab-active::after {
            content: '';
            position: absolute;
            bottom: 2px;
            width: 1.25rem;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #818cf8);
            border-radius: 9999px;
        }
        #log-search-input:focus {
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
            border-color: #a5b4fc;
        }
        button:active { transform: scale(0.97); }
"""

def apply_premium_tailwind(text):
    """Upgrade legacy Tailwind classes to premium rounded variants."""
    replacements = [
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
    for old, new in replacements:
        text = text.replace(old, new)
    return text

body = apply_premium_tailwind(body)
script = apply_premium_tailwind(script)

# Next maintenance plan: show service type (serviceLabel on alerts)
if 'target-service-val' not in body:
    body = body.replace(
        '<div class="text-[10px] text-slate-400 font-bold">แผนการเปลี่ยนระยะถัดไป</div>\n'
        '                    <div class="text-xs font-bold text-slate-700 mt-1.5" id="target-odometer-val">-</div>',
        '<div class="text-[10px] text-slate-400 font-bold">แผนการเปลี่ยนระยะถัดไป</div>\n'
        '                    <div class="text-[10px] text-indigo-700 font-bold mt-1" id="target-service-val">-</div>\n'
        '                    <div class="text-xs font-bold text-slate-700 mt-1" id="target-odometer-val">-</div>',
        1,
    )

if 'function resolveAlertServiceLabel' not in script:
    script = script.replace(
        '        function selectVehicle(id) {',
        """        function resolveAlertServiceLabel(alert) {
            if (!alert) return 'บำรุงรักษาตามกำหนด';
            if (alert.serviceLabel) return alert.serviceLabel;
            if (alert.categoryId) {
                const cat = state.categories.find(c => c.id === alert.categoryId);
                if (cat) return cat.name;
            }
            const logs = state.maintenanceLogs.filter(
                l => l.vehicleId === alert.vehicleId && l.date === alert.lastUpdated && (l.alertKm > 0 || l.alertMonth > 0)
            );
            if (logs.length > 0) {
                const cat = state.categories.find(c => c.id === logs[0].category);
                if (cat) return cat.name;
            }
            return 'บำรุงรักษาตามกำหนด';
        }

        function selectVehicle(id) {""",
        1,
    )

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

index_html = f'''<!DOCTYPE html>
<html lang="th" class="h-full min-h-full bg-slate-100 sm:bg-slate-200/80">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>MyHome CarCare - ระบบบำรุงรักษาและบันทึกน้ำมันสไตล์ Fuelio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        premium: {{
                            gold: '#c9a227',
                            champagne: '#f5ead6',
                            navy: '#0c0a1d',
                        }},
                    }},
                    borderRadius: {{
                        '4xl': '2rem',
                        '5xl': '2.5rem',
                    }},
                    boxShadow: {{
                        premium: '0 4px 24px rgba(15, 23, 42, 0.07), 0 1px 3px rgba(99, 102, 241, 0.05)',
                        'premium-lg': '0 20px 60px rgba(15, 23, 42, 0.12), 0 4px 16px rgba(201, 162, 39, 0.08)',
                        'premium-glow': '0 0 0 1px rgba(255,255,255,0.08), 0 8px 32px rgba(79, 70, 229, 0.18)',
                    }},
                }},
                screens: {{
                    xs: '400px',
                    sm: '640px',
                    md: '768px',
                    lg: '1024px',
                    xl: '1280px',
                    '2xl': '1536px',
                }},
            }},
        }};
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Itim&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
{inline_styles}
    </style>
</head>
<body class="app-shell relative">
{body}
    <script>
{script}
    </script>
</body>
</html>
'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(index_html)

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

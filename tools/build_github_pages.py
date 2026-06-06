"""Build static index.html for GitHub Pages from mockup + responsive GAS shell."""
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

# Version badge
body = re.sub(
    r'v[\d.]+ \([^)]+\)',
    'v2.0.0 (GitHub Pages)',
    body,
    count=1
)

# Remove loading overlay (instant localStorage app)
body = re.sub(
    r'\s*<div id="loading-overlay"[^>]*>.*?</div>\s*',
    '',
    body,
    count=1,
    flags=re.DOTALL
)

# Dynamic year options
current_year = datetime.now().year
year_options = ''.join(
    f'<option value="{y}">พ.ศ. {y + 543}</option>\n                        '
    for y in range(current_year, current_year - 5, -1)
)
body = re.sub(
    r'<select id="report-year-filter"[^>]*>.*?</select>',
    '<select id="report-year-filter" onchange="renderReports()" class="text-[11px] font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 rounded-lg px-2 py-1 outline-none focus:ring-1 focus:ring-indigo-500">\n                        '
    + year_options + '</select>',
    body,
    count=1,
    flags=re.DOTALL
)

# --- Patch JavaScript for v2.0 GitHub Pages ---
script = script.replace(
    "localStorage.getItem('myhome_carcare_state_v1.7')",
    "localStorage.getItem('myhome_carcare_state_v2.0')"
)
script = script.replace(
    "localStorage.setItem('myhome_carcare_state_v1.7', JSON.stringify(state));",
    "localStorage.setItem('myhome_carcare_state_v2.0', JSON.stringify(state));"
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
                return String(new Date(l.date).getFullYear()) === String(year);
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
                '<style>body{font-family:Sarabun,Arial,sans-serif;padding:24px;color:#1e293b}' +
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
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

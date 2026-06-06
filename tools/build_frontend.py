import re
import os

mockup_path = r'C:\Users\User\OWN_CAR PM\mockup\MyHome-CarCare-v1.8.html'
gas_dir = r'C:\Users\User\OWN_CAR PM\gas'

with open(mockup_path, 'r', encoding='utf-8') as f:
    html = f.read()

style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
styles = style_match.group(1) if style_match else ''

script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
script = script_match.group(1) if script_match else ''

body_match = re.search(r'<body[^>]*>(.*?)<script>', html, re.DOTALL)
body = body_match.group(1).strip() if body_match else ''

pdf_btn = '''
            <div class="pt-2">
                <button onclick="exportReportPdf()" class="w-full bg-slate-800 hover:bg-slate-900 text-white text-[11px] font-bold py-2.5 px-3 rounded-xl transition-all flex items-center justify-center gap-1.5 shadow-sm active:scale-95">
                    <i class="fa-solid fa-file-pdf text-rose-300"></i> ส่งออกรายงาน PDF รายปี
                </button>
            </div>'''

body = body.replace(
    '</section>\n\n        <!-- Live Maintenance History Logs -->',
    pdf_btn + '\n        </section>\n\n        <!-- Live Maintenance History Logs -->',
    1
)

loading_overlay = '''
    <div id="loading-overlay" class="hidden fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-[60] flex items-center justify-center">
        <div class="bg-white rounded-2xl px-6 py-4 shadow-2xl flex items-center gap-3">
            <i class="fa-solid fa-circle-notch fa-spin text-indigo-600 text-xl"></i>
            <span class="text-xs font-bold text-slate-700" id="loading-text">กำลังโหลด...</span>
        </div>
    </div>
'''
body = loading_overlay + '\n' + body

body = re.sub(
    r'<div class="lg:grid lg:grid-cols-2[^"]*"[^>]*>',
    '<div class="dashboard-grid space-y-4 sm:space-y-5 lg:space-y-0">',
    body,
    count=1
)

from datetime import datetime
current_year = datetime.now().year
year_options = ''.join(
    f'<option value="{y}">พ.ศ. {y + 543}</option>\n                        '
    for y in range(current_year, current_year - 5, -1)
)

body = re.sub(
    r'<select id="report-year-filter"[^>]*>.*?</select>',
    '<select id="report-year-filter" onchange="renderReportStats()" class="text-[11px] font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 rounded-lg px-2 py-1 outline-none focus:ring-1 focus:ring-indigo-500"></select>',
    body,
    count=1,
    flags=re.DOTALL
)

INLINE_STYLES = '''    <style>
        html {
            -webkit-text-size-adjust: 100%;
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background-color: #f1f5f9;
        }
        body {
            font-family: 'Inter', 'Sarabun', sans-serif;
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
            margin: 0;
            padding: 0;
            background-color: #f1f5f9;
        }
        @media (min-width: 640px) {
            html, body { background-color: rgba(226, 232, 240, 0.8); }
        }
        .app-shell {
            width: 100%;
            max-width: 100%;
            margin: 0 auto;
            min-height: 100vh;
            min-height: 100dvh;
            display: flex;
            flex-direction: column;
            background-color: #f8fafc;
            padding-left: env(safe-area-inset-left, 0);
            padding-right: env(safe-area-inset-right, 0);
            padding-bottom: env(safe-area-inset-bottom, 0);
        }
        @media (min-width: 640px) {
            .app-shell {
                max-width: 36rem;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
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
                border-radius: 1rem;
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
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
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
            animation: slide-up 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @media (min-width: 640px) {
            @keyframes slide-up-center {
                from { transform: translateY(16px) scale(0.98); opacity: 0; }
                to { transform: translateY(0) scale(1); opacity: 1; }
            }
            .modal-sheet-inner.animate-slide-up { animation-name: slide-up-center; }
        }
        .modal-sheet-inner { width: 100%; }
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
                gap: 0.75rem;
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
            .tab-content > section { transition: box-shadow 0.2s ease; }
        }
        @media (min-width: 1280px) {
            #vehicles-carousel { grid-template-columns: repeat(4, 1fr); }
        }
        #loading-overlay.hidden { display: none !important; }
    </style>'''

# Styles.html is no longer included at runtime (GAS include() leaks raw CSS in production).
# Keep a stub file so clasp push does not break if the file is referenced elsewhere.
with open(os.path.join(gas_dir, 'Styles.html'), 'w', encoding='utf-8') as f:
    f.write('<!-- Styles inlined in Index.html head — do not include via <?!= include() ?> -->\n')

index = '''<!DOCTYPE html>
<html lang="th" class="h-full min-h-full bg-slate-100 sm:bg-slate-200/80">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>MyHome CarCare - ระบบบำรุงรักษาและบันทึกน้ำมันสไตล์ Fuelio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                screens: {
                    xs: '400px',
                    sm: '640px',
                    md: '768px',
                    lg: '1024px',
                    xl: '1280px',
                    '2xl': '1536px',
                },
            },
        };
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
''' + INLINE_STYLES + '''
</head>
<body class="app-shell relative">
''' + body + '''
    <?!= include('Scripts'); ?>
</body>
</html>'''

with open(os.path.join(gas_dir, 'Index.html'), 'w', encoding='utf-8') as f:
    f.write(index)

# --- Patch script for GAS ---
API_LAYER = '''
        // --- Google Apps Script API layer ---
        function showLoading(msg) {
            const el = document.getElementById('loading-overlay');
            const txt = document.getElementById('loading-text');
            if (txt) txt.textContent = msg || 'กำลังโหลด...';
            if (el) el.classList.remove('hidden');
        }

        function hideLoading() {
            const el = document.getElementById('loading-overlay');
            if (el) el.classList.add('hidden');
        }

        function runGas(fn, args, onSuccess, onError) {
            showLoading();
            const runner = google.script.run
                .withSuccessHandler(function(result) {
                    hideLoading();
                    if (result && result.success === false) {
                        showToast(result.error || 'เกิดข้อผิดพลาด', 'error');
                        if (onError) onError(result);
                        return;
                    }
                    if (onSuccess) onSuccess(result);
                })
                .withFailureHandler(function(err) {
                    hideLoading();
                    showToast(err.message || String(err), 'error');
                    if (onError) onError(err);
                });
            if (args === undefined) runner[fn]();
            else if (Array.isArray(args)) runner[fn].apply(runner, args);
            else runner[fn](args);
        }

        function applyState(newState) {
            if (!newState) return;
            const adminAuth = state.adminAuthenticated;
            state = Object.assign({}, newState, { adminAuthenticated: adminAuth });
        }

        function refreshUI() {
            populateDropdowns();
            renderVehiclesCarousel();
            const vid = state.selectedVehicleId || (state.vehicles[0] && state.vehicles[0].id);
            if (vid) selectVehicle(vid);
            renderReports();
            initCustomCalendar();
            setDefaultDates();
        }

        function loadAppState(selectedId, callback) {
            runGas('getAppState', [selectedId || ''], function(result) {
                applyState(result);
                refreshUI();
                if (callback) callback(result);
            });
        }
'''

EXPORT_FN = '''
        function exportReportPdf() {
            const year = document.getElementById('report-year-filter').value;
            const vehicleId = state.selectedVehicleId;
            if (!vehicleId) {
                showToast('กรุณาเลือกรถก่อนส่งออกรายงาน', 'error');
                return;
            }
            showLoading('กำลังสร้าง PDF...');
            google.script.run
                .withSuccessHandler(function(result) {
                    hideLoading();
                    if (!result || !result.success) {
                        showToast((result && result.error) || 'ส่งออก PDF ไม่สำเร็จ', 'error');
                        return;
                    }
                    const link = document.createElement('a');
                    link.href = 'data:' + result.mimeType + ';base64,' + result.base64;
                    link.download = result.filename || 'report.pdf';
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    showToast('ดาวน์โหลดรายงาน PDF สำเร็จ');
                })
                .withFailureHandler(function(err) {
                    hideLoading();
                    showToast(err.message || String(err), 'error');
                })
                .exportReportPdf(vehicleId, year);
        }
'''

# Replace default state block
script = re.sub(
    r'let state = \{[\s\S]*?lineLogs:[\s\S]*?\};',
    '''let state = {
            vehicles: [],
            categories: [],
            maintenanceLogs: [],
            fuelLogs: [],
            alerts: [],
            selectedVehicleId: '',
            adminAuthenticated: false,
            lineLogs: [],
            lineNotifyConfigured: false,
            driveFolderId: ''
        };''' + API_LAYER,
    script,
    count=1
)

# Calendar defaults -> today
script = script.replace(
    'let calendarSelectedDate = new Date(2026, 5, 6); // Default 6 June 2026',
    'let calendarSelectedDate = new Date();'
)
script = script.replace('let calendarViewMonth = 5;', 'let calendarViewMonth = new Date().getMonth();')
script = script.replace('let calendarViewYear = 2026;', 'let calendarViewYear = new Date().getFullYear();')

# initApp
script = re.sub(
    r'function initApp\(\) \{[\s\S]*?switchTab\(\'dashboard\'\);\s*\}',
    """function initApp() {
            loadAppState('', function() {
                checkLineAlerts(false);
                switchTab('dashboard');
            });
        }""",
    script,
    count=1
)

# setDefaultDates
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
    'function saveToLocalStorage() {\n            localStorage.setItem(\'myhome_carcare_state_v1.7\', JSON.stringify(state));\n        }',
    'function saveToLocalStorage() { /* persisted in Google Sheets */ }'
)

# Modal date helpers - replace static June 2026 blocks only
for block in [
    """            calendarSelectedDate = new Date(2026, 5, 6);
            calendarViewMonth = 5; 
            calendarViewYear = 2026;
            syncCalendarDropdownSelectors();
            selectCalendarDate(6); // Force populate & sync the display field""",
]:
    script = script.replace(
        block,
        """            calendarSelectedDate = new Date();
            calendarViewMonth = calendarSelectedDate.getMonth();
            calendarViewYear = calendarSelectedDate.getFullYear();
            syncCalendarDropdownSelectors();
            selectCalendarDate(calendarSelectedDate.getDate());"""
    )

script = script.replace(
    '            // Static Time context representation (June 6, 2026)\n            const today = new Date(2026, 5, 6);',
    '            const today = new Date();'
)

script = script.replace(
    'const isToday = day === 6 && calendarViewMonth === 5 && calendarViewYear === 2026;',
    'const today = new Date();\n                const isToday = day === today.getDate() && calendarViewMonth === today.getMonth() && calendarViewYear === today.getFullYear();'
)

# saveOdometerOnly
script = re.sub(
    r'function saveOdometerOnly\(e\) \{[\s\S]*?checkLineAlerts\(true\);\s*\}',
    """function saveOdometerOnly(e) {
            e.preventDefault();
            const vId = document.getElementById('odo-vehicle-select').value;
            const odoVal = parseInt(document.getElementById('odo-mileage-input').value);
            const lastOdo = getLatestOdometer(vId);
            if (odoVal < lastOdo) {
                showToast("กิโลเมตรปัจจุบันน้อยกว่าครั้งล่าสุด!", "error");
                return;
            }
            runGas('saveOdometerOnly', { vehicleId: vId, odo: odoVal }, function(result) {
                applyState(result.state);
                closeModal('odometer-modal');
                showToast("อัปเดตระยะกิโลเมตรเรียบร้อยแล้ว");
                refreshUI();
                if (result.alertCheck && result.alertCheck.notificationTriggered) {
                    showLineBubble((result.alertCheck.messages || []).join(String.fromCharCode(10)));
                    showToast("LINE แจ้งเตือนครอบครัวเรียบร้อย!", "warning");
                }
            });
        }""",
    script,
    count=1
)

# saveMaintenanceLog
script = re.sub(
    r'function saveMaintenanceLog\(e\) \{[\s\S]*?renderReports\(\);\s*\n        \}',
    """function saveMaintenanceLog(e) {
            e.preventDefault();
            const vId = document.getElementById('rep-vehicle-select').value;
            const odoVal = parseInt(document.getElementById('rep-mileage').value);
            let category = document.getElementById('rep-category').value;
            const cost = parseFloat(document.getElementById('rep-cost').value);
            const shop = document.getElementById('rep-shop').value;
            const receiptInput = document.getElementById('rep-receipt');
            const repairDate = document.getElementById('rep-date').value || new Date().toISOString().split('T')[0];
            const lastOdo = getLatestOdometer(vId);
            if (odoVal < lastOdo) {
                showToast("เลขไมล์ปัจจุบันต่ำกว่าไมล์ครั้งล่าสุด!", "error");
                return;
            }
            let otherCategoryName = '';
            if (category === 'OTHER') {
                otherCategoryName = document.getElementById('rep-category-other').value.trim();
                if (!otherCategoryName) {
                    showToast("กรุณาระบุประเภทงานซ่อมอื่นๆ", "error");
                    return;
                }
            }
            let receiptName = '';
            let receiptBase64 = '';
            let receiptMimeType = '';
            if (receiptInput.files && receiptInput.files[0]) {
                const file = receiptInput.files[0];
                receiptName = file.name;
                receiptMimeType = file.type;
                receiptBase64 = currentUploadedReceiptBase64;
            }
            const alertKmEnabled = document.getElementById('alert-km-enable').checked;
            const alertMonthEnabled = document.getElementById('alert-month-enable').checked;
            const alertKm = alertKmEnabled ? parseInt(document.getElementById('alert-km-offset').value) : 0;
            const alertMonth = alertMonthEnabled ? parseInt(document.getElementById('alert-month-offset').value) : 0;
            runGas('saveMaintenanceLog', {
                vehicleId: vId,
                odo: odoVal,
                category: category,
                otherCategoryName: otherCategoryName,
                cost: cost,
                shop: shop,
                date: repairDate,
                alertKm: alertKm,
                alertMonth: alertMonth,
                receiptName: receiptName,
                receiptBase64: receiptBase64,
                receiptMimeType: receiptMimeType
            }, function(result) {
                applyState(result.state);
                closeModal('repair-modal');
                showToast("บันทึกการซ่อมบำรุงเรียบร้อย");
                document.getElementById('repair-form').reset();
                currentUploadedReceiptBase64 = "";
                document.getElementById('receipt-upload-preview').innerHTML = `
                    <i class="fa-solid fa-cloud-arrow-up text-lg text-indigo-500 mb-1"></i>
                    <div class="text-[9px] font-bold">แตะเพื่อถ่ายภาพหรือเลือกใบเสร็จรับเงิน</div>
                `;
                toggleAlertInputs();
                setDefaultDates();
                refreshUI();
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function saveFuelLog\(e\) \{[\s\S]*?renderFuelLogs\(\);\s*\n        \}',
    """function saveFuelLog(e) {
            e.preventDefault();
            const payload = {
                vehicleId: document.getElementById('fuel-vehicle-select').value,
                odo: parseInt(document.getElementById('fuel-odo').value),
                liters: parseFloat(document.getElementById('fuel-liters').value),
                pricePerLiter: parseFloat(document.getElementById('fuel-price-liter').value),
                totalCost: parseFloat(document.getElementById('fuel-total-cost').value),
                fullTank: document.getElementById('fuel-full-tank').checked,
                date: document.getElementById('fuel-date').value || new Date().toISOString().split('T')[0],
                fuelType: document.getElementById('fuel-type-input').value
            };
            const lastOdo = getLatestOdometer(payload.vehicleId);
            if (payload.odo < lastOdo) {
                showToast("ระยะไมล์ปัจจุบันน้อยกว่าระยะล่าสุดของรถ!", "error");
                return;
            }
            runGas('saveFuelLog', payload, function(result) {
                applyState(result.state);
                closeModal('fuel-modal');
                const typeLabelText = payload.fuelType === 'gas' ? 'แก๊ส (GAS)' : 'น้ำมัน';
                showToast('บันทึกประวัติการเติม' + typeLabelText + ' เรียบร้อยแล้ว');
                refreshUI();
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function deleteFuelLog\(id\) \{[\s\S]*?renderFuelLogs\(\);\s*\n        \}',
    """function deleteFuelLog(id) {
            runGas('deleteFuelLog', id, function(result) {
                applyState(result.state);
                showToast("ลบบันทึกเติมน้ำมันสำเร็จ", "warning");
                renderFuelLogs();
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function checkLineAlerts\(isManual = false\) \{[\s\S]*?saveToLocalStorage\(\);\s*\n        \}',
    """function checkLineAlerts(isManual = false) {
            runGas('checkLineAlerts', isManual, function(result) {
                if (result && result.state) applyState(result.state);
                if (result.notificationTriggered) {
                    showLineBubble((result.messages || []).join(String.fromCharCode(10)));
                    showToast(result.lineNotifyConfigured ? "LINE แจ้งเตือนครอบครัวเรียบร้อย!" : "แจ้งเตือน (โหมดจำลอง) เรียบร้อย!", "warning");
                } else if (isManual) {
                    showToast("รถทุกคันอยู่ในสภาพปกติและปลอดภัย");
                }
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function authenticateAdmin\(\) \{[\s\S]*?\n        \}',
    """function authenticateAdmin() {
            const user = document.getElementById('admin-username').value.trim();
            const pass = document.getElementById('admin-passcode').value;
            runGas('verifyAdmin', { username: user, password: pass }, function(result) {
                if (result.authenticated) {
                    state.adminAuthenticated = true;
                    showToast("ยินดีต้อนรับแอดมินบ้าน เข้าสู่โหมดควบคุมแล้ว");
                    renderAdminPanelState();
                } else {
                    showToast(result.message || "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง! (admin / 1234)", "error");
                }
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r"function saveVehicleEditAdmin\(e, id\) \{[\s\S]*?showToast\('[^']*'\);\s*\n        \}",
    """function saveVehicleEditAdmin(e, id) {
            e.preventDefault();
            const name = document.getElementById(`edit-car-name-${id}`).value.trim();
            const license = document.getElementById(`edit-car-license-${id}`).value.trim();
            if (!name || !license) {
                showToast('กรุณากรอกชื่อรถและทะเบียน', 'error');
                return;
            }
            const prbEl = document.getElementById(`edit-car-prb-${id}`);
            const insEl = document.getElementById(`edit-car-insurance-${id}`);
            runGas('updateVehicle', {
                id: id,
                name: name,
                license: license,
                selectedVehicleId: state.selectedVehicleId,
                prbExpiryDate: prbEl ? prbEl.value : '',
                insuranceExpiryDate: insEl ? insEl.value : ''
            }, function(result) {
                adminVehicleEditId = null;
                applyState(result.state);
                renderAdminVehicles();
                refreshUI();
                if (state.selectedVehicleId === id) {
                    selectVehicle(id);
                }
                showToast('บันทึกข้อมูลรถสำเร็จ');
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function addVehicleAdmin\(e\) \{[\s\S]*?showToast\("[^"]*"\);\s*\n        \}',
    """function addVehicleAdmin(e) {
            e.preventDefault();
            const name = document.getElementById('add-car-name').value.trim();
            const license = document.getElementById('add-car-license').value.trim();
            if (!name || !license) {
                showToast('กรุณากรอกชื่อรถและทะเบียน', 'error');
                return;
            }
            const prbDate = document.getElementById('add-car-prb-expiry').value;
            const insDate = document.getElementById('add-car-insurance-expiry').value;
            const payload = { name: name, license: license };
            if (prbDate) payload.prbExpiryDate = prbDate;
            if (insDate) payload.insuranceExpiryDate = insDate;
            runGas('addVehicle', payload, function(result) {
                applyState(result.state);
                document.getElementById('add-car-name').value = '';
                document.getElementById('add-car-license').value = '';
                document.getElementById('add-car-prb-expiry').value = '';
                document.getElementById('add-car-insurance-expiry').value = '';
                renderAdminVehicles();
                refreshUI();
                showToast("เพิ่มข้อมูลรถยนต์คันใหม่สำเร็จ");
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function deleteVehicleAdmin\(id\) \{[\s\S]*?showToast\("[^"]*"\);\s*\n        \}',
    """function deleteVehicleAdmin(id) {
            runGas('deleteVehicle', id, function(result) {
                applyState(result.state);
                renderAdminVehicles();
                refreshUI();
                showToast("ลบรถสำเร็จ");
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function addCategoryAdmin\(e\) \{[\s\S]*?showToast\("[^"]*"\);\s*\n        \}',
    """function addCategoryAdmin(e) {
            e.preventDefault();
            const name = document.getElementById('add-cat-name').value;
            runGas('addCategory', { name: name }, function(result) {
                applyState(result.state);
                document.getElementById('add-cat-name').value = '';
                renderAdminCategories();
                populateDropdowns();
                showToast("เพิ่มประเภทบริการสำเร็จ");
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function deleteCategoryAdmin\(id\) \{[\s\S]*?showToast\("[^"]*"\);\s*\n        \}',
    """function deleteCategoryAdmin(id) {
            runGas('deleteCategory', id, function(result) {
                applyState(result.state);
                renderAdminCategories();
                populateDropdowns();
                showToast("ลบประเภทเรียบร้อย");
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function saveEditedLog\(e\) \{[\s\S]*?renderReports\(\);\s*\n        \}',
    """function saveEditedLog(e) {
            e.preventDefault();
            const logId = document.getElementById('edit-log-id').value;
            const log = state.maintenanceLogs.find(l => l.id === logId);
            const payload = {
                id: logId,
                odo: parseInt(document.getElementById('edit-log-odo').value)
            };
            if (log && log.type !== 'Odometer_Update') {
                payload.shop = document.getElementById('edit-log-shop').value || '-';
                payload.cost = parseFloat(document.getElementById('edit-log-cost').value);
            } else {
                payload.shop = '-';
                payload.cost = 0;
            }
            runGas('saveEditedLog', payload, function(result) {
                applyState(result.state);
                closeModal('edit-log-modal');
                showToast("แก้ไขข้อมูลการซ่อมบำรุงสำเร็จ");
                refreshUI();
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function confirmDeleteLog\(logId\) \{[\s\S]*?renderReports\(\);\s*\n        \}',
    """function confirmDeleteLog(logId) {
            const log = state.maintenanceLogs.find(l => l.id === logId);
            if (!log) return;
            const label = log.type === 'Odometer_Update' ? 'รายการอัปเดตเลขไมล์' : 'รายการซ่อมบำรุง';
            if (!confirm(`ยืนยันลบ${label}นี้จากประวัติ?`)) return;
            runGas('deleteMaintenanceLog', logId, function(result) {
                applyState(result.state);
                showToast('ลบรายการออกจากบันทึกสำเร็จ', 'warning');
                refreshUI();
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function deleteMaintenanceLog\(\) \{[\s\S]*?renderReports\(\);\s*\n        \}',
    """function deleteMaintenanceLog() {
            const logId = document.getElementById('edit-log-id').value;
            runGas('deleteMaintenanceLog', logId, function(result) {
                applyState(result.state);
                closeModal('edit-log-modal');
                showToast("ลบรายการออกจากบันทึกสำเร็จ", "warning");
                refreshUI();
            });
        }""",
    script,
    count=1
)

script = re.sub(
    r'function showLineLogs\(\) \{[\s\S]*?\n        \}',
    """function showLineLogs() {
            const consoleEl = document.getElementById('line-api-console-log');
            if (!consoleEl) return;
            consoleEl.innerHTML = (state.lineLogs || []).map(l => '<div>' + l + '</div>').join('');
            const bubbleLabel = document.querySelector('#line-notification-bubble span.font-extrabold');
            if (bubbleLabel) {
                bubbleLabel.textContent = state.lineNotifyConfigured ? 'LINE NOTIFY (จริง)' : 'LINE NOTIFY (ครอบครัว)';
            }
            document.getElementById('line-logs-modal').classList.remove('hidden');
        }""",
    script,
    count=1
)

script = script.replace(
    'window.onload = function () {',
    EXPORT_FN + '\n        window.onload = function () {'
)

required = ['function initApp', 'function showToast', 'function selectVehicle', 'function renderFuelLogs', 'function openRepairModal', 'function exportReportPdf']
missing = [r for r in required if r not in script]
if missing:
    raise SystemExit('Missing functions after patch: ' + ', '.join(missing))

with open(os.path.join(gas_dir, 'Scripts.html'), 'w', encoding='utf-8') as f:
    f.write('<script>\n' + script + '\n</script>\n')

print('Generated frontend files OK')

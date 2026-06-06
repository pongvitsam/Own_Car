# MyHome CarCare

Family vehicle maintenance and Fuelio-style fuel logging.

## GitHub Pages (standalone)

| Item | Value |
|------|-------|
| **Live URL** | https://pongvitsam.github.io/Own_Car/ |
| **Repo** | https://github.com/pongvitsam/Own_Car |
| **Backend** | `localStorage` (browser-only, no server) |
| **Admin passcode** | `1234` |

Single-file `index.html` with **inline CSS** (fixes GAS `include('Styles')` leak). Data persists in the browser under key `myhome_carcare_state_v1.8`.

Rebuild after editing the mockup:

```bash
python tools/build_github_pages.py
```

## Google Apps Script (legacy)

Production web app backed by Google Sheets.

| Item | Value |
|------|-------|
| **Script ID** | `1tsg7o2-CdwWbaOhGLfoiDhuQfVn0ZelhucQOtSX9K9do8CNfMEEt1U70` |
| **Production URL** | https://script.google.com/macros/s/AKfycbzIZEXwdIsE0-uyh7VmejOEfPPWQSO2PxpyoJDuMmqWKkOcDN0swpzKBJjdcVSyinCwtw/exec |
| **Deployment ID** | `AKfycbzIZEXwdIsE0-uyh7VmejOEfPPWQSO2PxpyoJDuMmqWKkOcDN0swpzKBJjdcVSyinCwtw` |
| **Deploy version** | `@14` (spreadsheet permission fix + Thai errors + ownerBootstrapOnce) |
| **Receipts folder** | `1R-dpki8-nS17XAma6tyiQMEH66kEcf7U` |
| **Timezone** | Asia/Bangkok |
| **Admin passcode (default)** | `1234` |

## Features

- 3 tabs: Maintenance dashboard, Fuel (Fuelio), Admin
- Google Spreadsheet backend (auto-created on first run) with **update-not-duplicate** CRUD
- Receipt upload to Google Drive folder
- LINE Notify (free) when token is set; simulation UI + logs when not
- Daily auto-alert trigger (`dailyCheckAlerts` at 08:00)
- PDF export of yearly maintenance report
- Multi-user web app (no extra login gate when anonymous access is active)
- First-load welcome toast with setup hints (admin trigger, LINE token)

## Project structure

```
├── .clasp.json
├── package.json          # npm test script
├── lib/car-logic.js      # Shared formulas (npm test source of truth)
├── tests/car-logic.test.js
├── gas/
│   ├── Code.gs           # doGet, getAppState API
│   ├── Config.gs         # properties, constants
│   ├── Sheets.gs         # spreadsheet CRUD
│   ├── Vehicles.gs, Categories.gs, Maintenance.gs, Fuel.gs, Odometer.gs
│   ├── Alerts.gs, LineNotify.gs, Drive.gs, Admin.gs, Export.gs
│   ├── Index.html, Scripts.html, Styles.html
│   └── appsscript.json   # ANYONE_ANONYMOUS webapp access
├── tools/build_frontend.py
├── mockup/MyHome-CarCare-v1.8.html
└── README.md
```

> **Note:** Keep only `.gs` files in `gas/` — do not commit `.js` duplicates from `clasp pull`.

## Unit tests (local)

Pure logic in `lib/car-logic.js` mirrors GAS formulas (odometer, health bar, Fuelio metrics, alerts):

```bash
cd "C:\Users\User\OWN_CAR PM"
npm test
```

Expected: **29 tests pass** (6 suites).

## Setup checklist (owner — do once)

Use this after first deploy or when sharing with family:

- [ ] **Push code:** `clasp push -f` from project root
- [ ] **Redeploy Web App** (required after changing `appsscript.json` access settings):
  ```bash
  clasp deploy -i AKfycbzIZEXwdIsE0-uyh7VmejOEfPPWQSO2PxpyoJDuMmqWKkOcDN0swpzKBJjdcVSyinCwtw -d "MyHome CarCare production"
  ```
- [ ] **Anonymous access:** `gas/appsscript.json` must have `"access": "ANYONE_ANONYMOUS"`. Redeploy picks this up.
- [ ] **First OAuth (required):** Open the [Apps Script editor](https://script.google.com/home/projects/1tsg7o2-CdwWbaOhGLfoiDhuQfVn0ZelhucQOtSX9K9do8CNfMEEt1U70/edit), select `ownerBootstrapOnce` (or `getAppState`), click **Run**, and approve permissions (Sheets, Drive, UrlFetch for LINE). **Until this step completes, anonymous visitors get HTTP 403 or "You do not have permission to access the requested document."**
- [ ] **Open Web App URL once** (logged in as script owner) so the Spreadsheet and seed data are created.
- [ ] **Daily trigger:** Run `setupTriggers()` in the Apps Script editor, **or** Admin tab (passcode 1234) → **สร้าง Daily Trigger (08:00)**.
- [ ] **(Optional) LINE Notify token:** Apps Script → Project Settings → Script properties → add `LINE_NOTIFY_TOKEN` from [notify-bot.line.me](https://notify-bot.line.me/).
- [ ] **(Optional) Custom admin passcode:** Script property `ADMIN_PASS` overrides default `1234`.
- [ ] **Share production URL** with family — no Google login required after owner OAuth + anonymous deploy.

## Deploy & verify

```bash
cd "C:\Users\User\OWN_CAR PM"
npm test
clasp push -f
clasp deploy -i AKfycbzIZEXwdIsE0-uyh7VmejOEfPPWQSO2PxpyoJDuMmqWKkOcDN0swpzKBJjdcVSyinCwtw -d "MyHome CarCare production"
```

Verify the web app (after owner OAuth, should return **200** and HTML containing `MyHome CarCare`):

```bash
curl.exe -s -L -o test.html -w "HTTP:%{http_code}\n" "https://script.google.com/macros/s/AKfycbzIZEXwdIsE0-uyh7VmejOEfPPWQSO2PxpyoJDuMmqWKkOcDN0swpzKBJjdcVSyinCwtw/exec"
findstr /C:"MyHome CarCare" test.html
```

**Current curl status (2026-06-06, @14):** Production returns **HTTP 403** until the script owner (`rb2.emd@gmail.com`) completes first OAuth (`ownerBootstrapOnce` in editor). This is expected — not a code bug.

## API (google.script.run)

| Function | Description |
|----------|-------------|
| `getAppState(selectedVehicleId?)` | Full app state JSON |
| `saveOdometerOnly(data)` | Odometer-only update |
| `saveMaintenanceLog(data)` | Maintenance + receipt upload |
| `saveFuelLog(data)` | Fuel log |
| `deleteFuelLog(id)` | Delete fuel entry |
| `saveEditedLog(data)` | Edit maintenance log |
| `deleteMaintenanceLog(id)` | Delete maintenance log |
| `verifyAdmin(passcode)` | Admin auth |
| `addVehicle` / `deleteVehicle` | Admin vehicles |
| `addCategory` / `deleteCategory` | Admin categories |
| `checkLineAlerts(manual)` | Manual/auto alert check |
| `exportReportPdf(vehicleId, year)` | PDF base64 download |
| `setupTriggers()` | Create daily trigger |
| `dailyCheckAlerts()` | Trigger handler |

## Sheet schema (Thai names)

| Sheet | Columns |
|-------|---------|
| รถ | vehicleId, ชื่อ, ทะเบียน, สร้างเมื่อ |
| หมวดซ่อม | categoryId, ชื่อ |
| บันทึกซ่อม | logId, vehicleId, วันที่, categoryId, ร้าน, ราคา, ไมล์, type, alertKm, alertMonth, driveFileId, driveUrl, receiptName |
| เติมเชื้อเพลิง | logId, vehicleId, วันที่, fuelType, ไมล์, ลิตร, ราคา/ลิตร, ราคารวม, เต็มถัง, สถานี |
| แจ้งเตือน | alertId, vehicleId, targetKm, targetDate, status, lastUpdated |
| ตั้งค่า | key, value |

## Rebuild frontend from mockup

```bash
python tools/build_frontend.py
clasp push -f
```

## Troubleshooting

- **403 / “ต้องการสิทธิ์เข้าถึง” / “You do not have permission to access the requested document”:** Deploy must use **Execute as: Me** (`USER_DEPLOYING` in `appsscript.json`) and **Who has access: Anyone** (`ANYONE_ANONYMOUS`). Redeploy after changing manifest. Then run `ownerBootstrapOnce` once in the Apps Script editor as owner (`rb2.emd@gmail.com`) to grant OAuth and create the spreadsheet.
- **CSS shows as plain text:** Ensure `Index.html` uses `<?!= include('Styles'); ?>` and `Styles.html` wraps rules in `<style>...</style>` (fixed in v1.8).
- **Drive upload fails:** Ensure the script owner has write access to folder `1R-dpki8-nS17XAma6tyiQMEH66kEcf7U`.
- **PDF export empty:** Grant script authorization when prompted on first export.
- **LINE not sending:** Verify `LINE_NOTIFY_TOKEN` in Script Properties; check LINE log modal in app (simulation mode when token is empty).
- **Trigger not firing:** Run `setupTriggers()` once as script owner; check Triggers page in Apps Script editor.
- **Duplicate `.js` in `gas/`:** Delete them after `clasp pull`; keep only `.gs` sources.

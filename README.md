# MyHome CarCare

Family vehicle maintenance and Fuelio-style fuel logging — **static PWA on GitHub Pages (v3.2.0)**.

## Live

| Item | Value |
|------|-------|
| **Live URL** | https://pongvitsam.github.io/Own_Car/ |
| **Repo** | https://github.com/pongvitsam/Own_Car |
| **Storage** | `localStorage` key `myhome_carcare_state_v2.2` (browser-only) |
| **Admin** | `admin` / `1234` |
| **PWA** | Installable (`manifest.webmanifest` + `sw.js`) |

## Features (v3.2)

- Maintenance dashboard, Fuelio fuel tab, Admin
- Side navigation (drawer on mobile, persistent sidebar on tablet/desktop)
- Fuelio summary: km driven, liters used, km/L (oil and gas as **separate** full-tank chains)
- Trend chart + family vehicle efficiency compare
- Edit / delete fuel logs; optional station name
- Export / Import JSON backup (Admin)
- Thai Buddhist Era dates, PDF yearly report
- LINE alert **simulation** on GitHub Pages (real LINE Notify via legacy GAS)

> Data lives in the browser. Use **Admin → Export JSON** before clearing cache or changing devices.

## Develop

```bash
cd "C:\Users\User\OWN_CAR PM"
npm test
python tools/build_github_pages.py
python tools/deploy_pages.py "Your commit message"
```

Expected: **113+ tests pass**.

## Project structure

```
├── index.html                 # Built GitHub Pages app
├── manifest.webmanifest       # PWA manifest
├── sw.js                      # Service worker
├── icons/icon.svg
├── mockup/MyHome-CarCare-v1.8.html   # Source UI + JS
├── tools/build_github_pages.py
├── tools/premium_ui.py
├── tools/deploy_pages.py
├── lib/car-logic.js           # Shared formulas (npm test source of truth)
├── tests/
└── gas/                       # Google Apps Script backend (Sheets sync + LINE)
```

## Google Apps Script (Sheets sync)

GitHub Pages connects to GAS via an **iframe Bridge** (`?bridge=1`) — the browser cannot call `google.script.run` cross-origin directly.

1. Open [Apps Script](https://script.google.com/home/projects/1mCIIW3agh-B14wqqR5nsyGEKYirHXa85NkGrCZGksuSljkyuyXcveNI8/edit) project (`.clasp.json`), then `clasp push` from this repo (`rootDir: gas`).
2. Run `ownerBootstrapOnce` once in the editor (creates Google Sheet + imports Mazda/Click/Altis).
3. **Deploy → Manage deployments → Edit**
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Copy the `/exec` URL.
5. On the live app → **Admin** → section **Google Sheets sync**
   - Paste URL → **ทดสอบการเชื่อมต่อ** → enable sync → **บันทึกการตั้งค่า**
6. Saves (fuel / maintenance / odo / vehicles) write to the Sheet; use **ดึงจาก Sheet** to refresh across devices.

Default Web App URL is baked into the UI; override anytime in Admin. Without sync enabled, the app stays on localStorage + Export/Import.

See also `gas/Bridge.html` and `gas/Api.gs` (`apiCall` / `getFullSyncState`).

## Troubleshooting

- **Data missing after browser clear:** Restore from Export JSON backup, or enable Sheets sync and pull.
- **Fuel efficiency blank:** Need two consecutive **full tank** fills of the **same** fuel type (oil or gas).
- **PWA not installing:** Open over HTTPS (GitHub Pages), hard-refresh, check Application → Manifest.
- **Deploy fails on Windows:** `tools/deploy_pages.py` resolves `npm.cmd` via shell — run `python tools/deploy_pages.py "msg"`.
- **Sheet sync fails / Bridge timeout:** Redeploy the Web App after `clasp push`, confirm “Anyone” access, and that the URL ends with `/exec`.
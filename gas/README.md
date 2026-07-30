# Google Apps Script backend (Sheets sync)

Used by the GitHub Pages app via **iframe Bridge** (`?bridge=1` + `postMessage` → `google.script.run.apiCall`).

## Setup

```bash
python tools/generate_gas_seed.py   # embeds family seed into gas/SeedData.gs
clasp push -f
clasp version "..."
clasp deploy -d "MyHome CarCare public Web App (Anyone)"
```

Current Script ID: `1mCIIW3agh-B14wqqR5nsyGEKYirHXa85NkGrCZGksuSljkyuyXcveNI8`

**One-time in Apps Script UI (required for public access + Sheet creation):**
1. Open [project editor](https://script.google.com/home/projects/1mCIIW3agh-B14wqqR5nsyGEKYirHXa85NkGrCZGksuSljkyuyXcveNI8/edit)
2. Run function `ownerBootstrapOnce` once → approve Sheets/Drive permissions
3. **Deploy → Manage deployments → Edit (✎)** the Web App  
   - Execute as: **Me**  
   - Who has access: **Anyone**  
   - Deploy / New version
4. Copy `/exec` URL into GitHub Pages Admin → Google Sheets sync

Family data imported: Mazda, Honda Click 160, Toyota Altis (88 maintenance logs).

Current Web App URL (clasp deploy):
`https://script.google.com/macros/s/AKfycbzn1_ZmKOk4gCjAEuhC_ZKG9Iuejlyt3U3o8qPg7qv2AqdHtXUjVadawjZ_zrldlI2Wrw/exec`

## Key files

| File | Role |
|------|------|
| `Bridge.html` | postMessage bridge for Pages |
| `Api.gs` | `apiCall`, `getFullSyncState`, HTTP `doPost` |
| `Code.gs` | `doGet` routes bridge / JSON API / Index |
| `Fuel.gs` / `Maintenance.gs` / … | Sheet CRUD |

Primary UI remains GitHub Pages: https://pongvitsam.github.io/Own_Car/

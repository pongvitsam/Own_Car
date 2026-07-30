# Google Apps Script backend (Sheets sync)

Used by the GitHub Pages app via **iframe Bridge** (`?bridge=1` + `postMessage` → `google.script.run.apiCall`).

## Setup

```bash
clasp push -f
```

Then in Apps Script UI: **Deploy → Manage deployments → Edit (pencil) → New version → Deploy**  
(or create a new Web App: Execute as **Me**, access **Anyone**).

Copy the `/exec` URL into the live app **Admin → Google Sheets sync**.

## Key files

| File | Role |
|------|------|
| `Bridge.html` | postMessage bridge for Pages |
| `Api.gs` | `apiCall`, `getFullSyncState`, HTTP `doPost` |
| `Code.gs` | `doGet` routes bridge / JSON API / Index |
| `Fuel.gs` / `Maintenance.gs` / … | Sheet CRUD |

Primary UI remains GitHub Pages: https://pongvitsam.github.io/Own_Car/

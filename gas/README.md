# Legacy Google Apps Script (deprecated)

This folder contains the original GAS web app backed by Google Sheets.

**Use the GitHub Pages app instead:** https://pongvitsam.github.io/Own_Car/

Known GAS issues:
- Slow server round-trips on every action
- Raw CSS text at top of page when using `<?!= include('Styles') ?>` (GAS strips `<style>` tags from includes)

To rebuild GAS frontend from mockup (if still needed):

```bash
python tools/build_frontend.py
clasp push -f
```

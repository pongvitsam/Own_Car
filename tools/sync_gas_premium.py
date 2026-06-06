"""Sync premium UI into gas/Index.html for GAS deployment."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from premium_ui import PREMIUM_INLINE_STYLES, apply_premium_html  # noqa: E402

gas = ROOT / 'gas' / 'Index.html'
text = gas.read_text(encoding='utf-8')
text = re.sub(
    r'<style>.*?</style>',
    f'<style>\n{PREMIUM_INLINE_STYLES.strip()}\n    </style>',
    text,
    count=1,
    flags=re.DOTALL,
)
text = text.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Itim&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
)
body_m = re.search(r'(<body[^>]*>)(.*?)(<\?!= include)', text, re.DOTALL)
if body_m:
    inner = apply_premium_html(body_m.group(2))
    text = text[: body_m.start(2)] + inner + text[body_m.end(2) :]
gas.write_text(text, encoding='utf-8')
print(f'Synced {gas}')

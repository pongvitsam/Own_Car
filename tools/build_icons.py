"""Build a trimmed, self-hosted Font Awesome subset (assets/fa-subset.css + webfonts).

One-time setup: cd tools/_fa && npm init -y && npm i @fortawesome/fontawesome-free@6.4.0
Re-run whenever new fa-* icons are used in the mockup.
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FA = os.path.join(ROOT, 'tools', '_fa', 'node_modules', '@fortawesome', 'fontawesome-free')
MOCKUP = os.path.join(ROOT, 'mockup', 'MyHome-CarCare-v1.8.html')
OUT_CSS = os.path.join(ROOT, 'assets', 'fa-subset.css')
OUT_FONTS = os.path.join(ROOT, 'assets', 'webfonts')

if not os.path.isdir(FA):
    raise SystemExit('Font Awesome not installed: cd tools/_fa && npm init -y && npm i @fortawesome/fontawesome-free@6.4.0')

with open(MOCKUP, encoding='utf-8') as f:
    html = f.read()
used = set(re.findall(r'\bfa-([a-z0-9-]+)', html))
used -= {'solid', 'regular', 'brands', 'spin'}

with open(os.path.join(FA, 'css', 'all.css'), encoding='utf-8') as f:
    css = f.read()

glyphs = []
for name in sorted(used):
    m = re.search(r'\.fa-' + re.escape(name) + r'::?before\s*\{\s*content:\s*"([^"]+)";?\s*\}', css)
    if not m:
        print('WARN: icon not in free set:', name)
        continue
    glyphs.append(f'.fa-{name}::before{{content:"{m.group(1)}"}}')

base = '''@font-face{font-family:"Font Awesome 6 Free";font-style:normal;font-weight:900;font-display:swap;src:url(./webfonts/fa-solid-900.woff2) format("woff2")}
@font-face{font-family:"Font Awesome 6 Free";font-style:normal;font-weight:400;font-display:swap;src:url(./webfonts/fa-regular-400.woff2) format("woff2")}
.fa-solid,.fa-regular{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;display:inline-block;font-style:normal;font-variant:normal;line-height:1;text-rendering:auto;font-family:"Font Awesome 6 Free"}
.fa-solid{font-weight:900}.fa-regular{font-weight:400}
.fa-spin{animation:fa-spin 2s linear infinite}
@keyframes fa-spin{0%{transform:rotate(0)}to{transform:rotate(360deg)}}
'''
os.makedirs(OUT_FONTS, exist_ok=True)
for name in ('fa-solid-900.woff2', 'fa-regular-400.woff2'):
    shutil.copy(os.path.join(FA, 'webfonts', name), os.path.join(OUT_FONTS, name))
with open(OUT_CSS, 'w', encoding='utf-8') as f:
    f.write(base + '\n'.join(glyphs) + '\n')
print(f'{len(glyphs)} icons -> {OUT_CSS}')

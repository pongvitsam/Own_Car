"""Build, test, commit, and push GitHub Pages deployment."""
import shutil
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKED = [
    'mockup/MyHome-CarCare-v1.8.html',
    'tools/premium_ui.py',
    'tools/build_github_pages.py',
    'tools/deploy_pages.py',
    'package.json',
    'index.html',
    'manifest.webmanifest',
    'sw.js',
    'icons/icon.svg',
    'README.md',
    'lib/car-logic.js',
    'tests/car-logic.test.js',
    'gas/Api.gs',
    'gas/Bridge.html',
    'gas/Code.gs',
    'gas/README.md',
]


def run(cmd, cwd=ROOT, shell=False):
    print(f'> {" ".join(cmd) if isinstance(cmd, list) else cmd}')
    result = subprocess.run(cmd, cwd=cwd, shell=shell)
    if result.returncode != 0:
        sys.exit(result.returncode)


def npm_cmd(*args):
    """Resolve npm on Windows (npm.cmd) and other platforms."""
    npm = shutil.which('npm') or shutil.which('npm.cmd')
    if not npm:
        print('ERROR: npm not found on PATH', file=sys.stderr)
        sys.exit(1)
    if os.name == 'nt':
        # Windows: use shell so .cmd wrappers resolve correctly
        quoted = ' '.join(f'"{a}"' if ' ' in a else a for a in [npm, *args])
        run(quoted, shell=True)
    else:
        run([npm, *args])


def main():
    if len(sys.argv) < 2:
        print('Usage: python tools/deploy_pages.py "commit message"', file=sys.stderr)
        sys.exit(1)

    message = sys.argv[1]

    run([sys.executable, 'tools/build_github_pages.py'])
    npm_cmd('test')

    existing = [f for f in TRACKED if os.path.exists(os.path.join(ROOT, f))]
    run(['git', 'add', *existing])
    run(['git', 'commit', '-m', message])
    run(['git', 'push', 'origin', 'main'])

    result = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    print(f'Deployed commit: {result.stdout.strip()}')


if __name__ == '__main__':
    main()

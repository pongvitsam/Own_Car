"""Build, test, commit, and push GitHub Pages deployment."""
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
]


def run(cmd, cwd=ROOT):
    print(f'> {" ".join(cmd)}')
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    if len(sys.argv) < 2:
        print('Usage: python tools/deploy_pages.py "commit message"', file=sys.stderr)
        sys.exit(1)

    message = sys.argv[1]

    run([sys.executable, 'tools/build_github_pages.py'])
    run(['npm', 'test'])

    run(['git', 'add', *TRACKED])
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

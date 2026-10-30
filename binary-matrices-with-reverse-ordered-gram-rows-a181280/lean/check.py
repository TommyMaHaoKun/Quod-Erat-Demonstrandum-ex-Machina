"""Compile the local Lean import closure sequentially using the pinned Lake environment."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

root = Path(__file__).resolve().parent
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
order, seen, active = [], set(), set()


def visit(name):
    if name in seen:
        return
    if name in active:
        raise RuntimeError(f"Import cycle at {name}")
    active.add(name)
    source = root / (name.replace('.', '/') + '.lean')
    for dependency in re.findall(r'^import\s+(MathLean(?:\.\w+)*)\s*$', source.read_text(encoding='utf-8-sig'), re.M):
        visit(dependency)
    active.remove(name)
    seen.add(name)
    order.append((name, source))


def run(arguments):
    result = subprocess.run(['lake', 'env', 'lean', *arguments], cwd=root,
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.stdout:
        print(result.stdout, end='', flush=True)
    if result.stderr:
        print(result.stderr, end='', file=sys.stderr, flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result


visit('MathLean')
if '--list' in sys.argv[1:]:
    print('\n'.join(name for name, _ in order))
    raise SystemExit(0)
run(['--version'])
build = root / '.lake' / 'build' / 'lib' / 'lean'
record = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'modules': []}
for name, source in order:
    relative = source.relative_to(root)
    output = build / relative.with_suffix('.olean')
    output.parent.mkdir(parents=True, exist_ok=True)
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    # Remove only this module's disposable output; never remove source or dependencies.
    if output.exists():
        output.unlink()
    print(f'Checking {relative.as_posix()}', flush=True)
    result = run(['-j', '1', '-o', str(output), str(relative)])
    after = hashlib.sha256(source.read_bytes()).hexdigest()
    if before != after:
        raise RuntimeError(f'Source changed during compilation: {relative}')
    record['modules'].append({'module': name, 'sha256': after, 'exit_code': result.returncode,
                              'output': result.stdout + result.stderr})
    (root / '.lake' / 'check-results.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print(f'PASS: {len(order)} modules, including the project root.', flush=True)

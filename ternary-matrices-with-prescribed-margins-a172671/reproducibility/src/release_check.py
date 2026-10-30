"""Run proof checks and rebuild in a clean location inside the project."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]

def main():
    (ROOT/'tmp').mkdir(exist_ok=True)
    clean = Path(tempfile.mkdtemp(prefix='release-', dir=ROOT/'tmp'))
    for folder in ('src', 'paper', 'literature', 'certificates', 'output'):
        (clean/folder).mkdir()
    needed = ['src/verify_certificate.py', 'src/route_alt_transfer.py',
              'src/independent_checks.py', 'paper/main.tex',
              'literature/target_formula.tex']
    for relative in needed:
        shutil.copyfile(ROOT/relative, clean/relative)
    results = []
    commands = [[sys.executable, 'src/'+name] for name in
                ('verify_certificate.py', 'route_alt_transfer.py', 'independent_checks.py')]
    commands += [['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                  '-output-directory=output', 'paper/main.tex']]*2
    for index, command in enumerate(commands):
        start = time.monotonic()
        run = subprocess.run(command, cwd=clean, capture_output=True, text=True,
                             encoding='utf-8', errors='replace', timeout=180)
        (clean/'output'/f'check-{index+1}.log').write_text(run.stdout+'\n'+run.stderr, encoding='utf-8')
        results.append({'step': index+1, 'command': ' '.join(command[1:]) if index < 3 else 'pdflatex pass '+str(index-2),
                        'returncode': run.returncode, 'seconds': round(time.monotonic()-start, 3)})
        if run.returncode:
            raise RuntimeError(f'Clean check {index+1} failed: {run.stdout[-4000:]} {run.stderr}')
    log = (clean/'output'/'main.log').read_text(encoding='utf-8', errors='replace')
    forbidden = ['Overfull', 'undefined references', 'undefined on input line', 'Rerun to get cross-references']
    assert not any(x in log for x in forbidden), [x for x in forbidden if x in log]
    assert (clean/'output'/'main.pdf').stat().st_size > 10000
    report = {'status': 'PASS', 'clean_directory': str(clean.relative_to(ROOT)),
              'steps': results, 'latex_warnings_checked': forbidden,
              'inputs_sha256': {p: hashlib.sha256((clean/p).read_bytes()).hexdigest() for p in needed},
              'scope': 'All proof verifiers and two LaTeX passes succeed from isolated relative-path inputs.'}
    (ROOT/'certificates'/'release_check.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()

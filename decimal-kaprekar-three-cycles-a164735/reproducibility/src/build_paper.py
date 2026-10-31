"""Compile the self-contained saved LaTeX source twice."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
(root/'output').mkdir(exist_ok=True)
command = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
           '-output-directory=../output', '-jobname=research_paper', 'main.tex']
for _ in range(2):
    result = subprocess.run(command, cwd=root/'paper', capture_output=True, text=True)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)
log = (root/'output'/'research_paper.log').read_text(errors='replace')
if 'Overfull' in log or 'undefined references' in log or 'undefined on input line' in log:
    raise SystemExit('Check LaTeX log: layout or references require review.')
print('PASS: output/research_paper.pdf compiled with resolved references.')

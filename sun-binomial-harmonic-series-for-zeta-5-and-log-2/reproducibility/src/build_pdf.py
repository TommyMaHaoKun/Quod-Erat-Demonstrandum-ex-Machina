"""Build the complete saved manuscript with a local pdfLaTeX installation."""
from pathlib import Path
import shutil
import subprocess
import hashlib

root = Path(__file__).resolve().parents[1]
compiler = shutil.which("pdflatex")
if compiler is None:
    raise SystemExit("Install a TeX distribution providing pdflatex and retry.")
output = root/"output"
output.mkdir(exist_ok=True)
args = [compiler,"-interaction=nonstopmode","-halt-on-error",
        "-jobname=research_paper","-output-directory=output","paper/main.tex"]
for _ in range(2):
    result = subprocess.run(args,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout.decode(errors="replace"))
        raise SystemExit(result.returncode)
log = (output/"research_paper.log").read_text(errors="replace")
for problem in ["Overfull", "There were undefined references", "Citation `", "Reference `"]:
    if problem in log:
        raise SystemExit("Resolve the LaTeX diagnostic before release: "+problem)
pdf = output/"research_paper.pdf"
print("Compiled:",pdf)
print("SHA-256:",hashlib.sha256(pdf.read_bytes()).hexdigest())

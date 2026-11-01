"""Compile the self-contained paper twice with an installed pdflatex."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    compiler = shutil.which("pdflatex")
    if not compiler:
        raise SystemExit("pdflatex is required (TeX Live or MiKTeX).")
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    command = [compiler, "-interaction=nonstopmode", "-halt-on-error",
               "-output-directory=" + str(output), "-jobname=research_paper", "main.tex"]
    for pass_number in (1, 2):
        result = subprocess.run(command, cwd=ROOT / "paper", capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
        if result.returncode:
            print(result.stdout)
            print(result.stderr)
            raise SystemExit(result.returncode)
        print("LaTeX pass", pass_number, "succeeded.")
    log = (output / "research_paper.log").read_text(encoding="utf-8", errors="replace")
    issues = [line for line in log.splitlines()
              if "undefined" in line.lower() or "Overfull" in line or "Underfull" in line]
    if issues:
        raise SystemExit("LaTeX quality check:\n" + "\n".join(issues))
    pdf = output / "research_paper.pdf"
    assert pdf.is_file() and pdf.stat().st_size > 0
    print("BUILT:", pdf)


if __name__ == "__main__":
    main()

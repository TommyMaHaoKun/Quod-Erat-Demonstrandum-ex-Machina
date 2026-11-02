"""Build the self-contained paper using pdflatex (twice) or Tectonic.

Run from any directory. The source is located relative to this script.
"""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "paper.pdf")
    args = parser.parse_args()
    source = root / "paper" / "main.tex"
    if not source.is_file():
        raise SystemExit("Missing paper/main.tex")
    pdflatex = shutil.which("pdflatex")
    tectonic = shutil.which("tectonic")
    if not pdflatex and not tectonic:
        raise SystemExit("Install pdflatex or Tectonic and put it on PATH.")
    temporary_parent = root / "tmp"
    temporary_parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="paper-build-", dir=temporary_parent) as work:
        work = Path(work)
        shutil.copy2(source, work / "main.tex")
        if pdflatex:
            command = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
            repetitions = 2
        else:
            command = [tectonic, "--keep-logs", "main.tex"]
            repetitions = 1
        for _ in range(repetitions):
            result = subprocess.run(command, cwd=work, capture_output=True, text=True,
                                    encoding="utf-8", errors="replace")
            if result.returncode:
                raise SystemExit(result.stdout + result.stderr)
        log = (work / "main.log").read_text(encoding="utf-8", errors="replace")
        failures = [pattern for pattern in ["Overfull", "Missing character:",
                    "There were undefined references", "undefined on input line"]
                    if pattern in log]
        if failures:
            raise SystemExit("LaTeX check failed: " + ", ".join(failures))
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(work / "main.pdf", output)
    print("PASS: compiled twice with pdflatex" if pdflatex else "PASS: compiled with Tectonic")
    print(output)


if __name__ == "__main__":
    main()

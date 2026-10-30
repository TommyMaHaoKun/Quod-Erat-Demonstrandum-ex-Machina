"""Run every verification script and write the certificate files.

Usage (from the folder that contains src/ and certificates/):
    python src/verify_all.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CERT = os.path.join(ROOT, "certificates")

STEPS = [
    ("verify_wz.py", "wz_symbolic.json"),
    ("verify_independent.py", "independent_exact.json"),
    ("numerical_checks.py", "numerical_enclosures.json"),
]


def main():
    os.makedirs(CERT, exist_ok=True)
    report = {}
    ok = True
    for script, name in STEPS:
        proc = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True)
        with open(os.path.join(CERT, name), "w", encoding="utf-8") as fh:
            fh.write(proc.stdout)
        try:
            status = json.loads(proc.stdout)["status"]
        except (ValueError, KeyError):
            status = "ERROR"
            sys.stderr.write(proc.stderr)
        report[script] = status
        ok = ok and proc.returncode == 0 and status == "PASS"
        print(f"{script}: {status}")
    report["overall"] = "PASS" if ok else "FAIL"
    with open(os.path.join(CERT, "verification_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")
    print("overall:", report["overall"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

"""Run every exact arithmetic check used by the all-n proof.

Requires Python 3.9 or later and its standard library only. Invoke this
file from any working directory; all package paths are resolved here.
Run without -O: the component verifiers use assertions as proof checks.
"""
import json
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
CERTIFICATE = ROOT / "certificates" / "sign_certificates_n1_250.json"

CHECKS = [
    ("exact sign certificates for 0 <= n <= 250", "verify_certificates.py", [str(CERTIFICATE)]),
    ("uniform variance through 4 sqrt(n)", "astra_literature/verify_extended_variance_constants.py", []),
    ("negative-s pole dominance through 4 sqrt(n)", "astra_structural/verify_negative_bulk_pole_constants_4sqrt.py", []),
    ("positive-s pole dominance through 3 sqrt(n)", "astra_structural/verify_positive_bulk_constants.py", []),
    ("positive-s pole dominance from 3 to 4 sqrt(n)", "astra_structural/verify_positive_bulk_extension_constants.py", []),
    ("joint tails and actual Eulerian errors", "astra_literature/verify_joint_tail_audit_constants.py", []),
    ("finite edge bridge for 250 <= n <= 1600", "astra_literature/verify_finite_edge_bridge.py", []),
    ("independent zeros and paired-cluster signs", "astra_structural/verify_paired_cluster_sign_constants.py", []),
    ("mode geometry and phase matching", "astra_interlacing/verify_mode_geometry_constants.py", []),
]


def main():
    if not __debug__ or sys.flags.optimize:
        raise SystemExit("Run this verifier without -O or PYTHONOPTIMIZE.")
    if sys.version_info < (3, 9):
        raise SystemExit("Python 3.9 or later is required.")
    with CERTIFICATE.open(encoding="utf-8") as stream:
        certificate = json.load(stream)
    if certificate.get("N") != 250:
        raise SystemExit("The finite certificate must cover every n through 250.")
    for _, relative, _ in CHECKS:
        if not (SRC / relative).is_file():
            raise SystemExit("Missing required verifier: " + relative)
    started = time.monotonic()
    for index, (description, relative, arguments) in enumerate(CHECKS, 1):
        print("[{}/{}] {}".format(index, len(CHECKS), description), flush=True)
        # -E ignores interpreter environment overrides; -B avoids cache files.
        subprocess.run(
            [sys.executable, "-E", "-B", str(SRC / relative)] + arguments,
            cwd=str(ROOT), check=True,
        )
    print("PASS: all {} proof checks ({:.1f} seconds)".format(
        len(CHECKS), time.monotonic()-started), flush=True)


if __name__ == "__main__":
    main()

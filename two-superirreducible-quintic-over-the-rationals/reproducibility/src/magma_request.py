"""Run a saved Magma program through the public calculator API.

Every source and response is saved together. In verification mode, an engine
failure returns a nonzero exit code. The mathematical assertions belong to
the supplied Magma program. The service publishes its limits at /info.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--purpose", choices=("exploration", "verification"), default="exploration")
    args = parser.parse_args()
    code = args.source.read_text(encoding="utf-8")
    response = requests.post(
        "https://calculator.magma-maths.org/execute",
        json={"code": code},
        timeout=320,
    )
    record = {
        "purpose": ("complete arithmetic verification" if args.purpose == "verification"
                    else "exploratory computation; assess output before any proof claim"),
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": args.source.name,
        "code": code,
        "source_sha256": hashlib.sha256(code.encode("utf-8")).hexdigest(),
        "http_status": response.status_code,
    }
    try:
        record["response"] = response.json()
    except ValueError:
        record["response_text"] = response.text
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    if args.purpose == "verification" and record.get("response", {}).get("success"):
        args.output.with_suffix(".log").write_text(record["response"]["stdout"], encoding="utf-8")
    print(json.dumps(record, indent=2))
    if args.purpose == "verification" and not record.get("response", {}).get("success"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

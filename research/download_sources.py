"""Cache the public research inputs; restart safely after an interrupted download."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request
import argparse

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "djm_data.zip": "https://openbondassetpricing.com/wp-content/uploads/2025/12/djm_data.zip",
    "ExcessLongShortVW_All_Databases.zip": "https://openbondassetpricing.com/wp-content/uploads/2025/07/ExcessLongShortVW_All_Databases.zip",
    "Factor_Time_Series_LongShort.zip": "https://openbondassetpricing.com/wp-content/uploads/2024/11/Factor_Time_Series_LongShort.zip",
}
REFERENCES = {
    "openbond_home.html": "https://openbondassetpricing.com/",
    "delays_2025.pdf": "https://www.ier.hit-u.ac.jp/Common/publication/DP/DPS-A771.pdf",
    "priced_risk_2023.pdf": "https://wrap.warwick.ac.uk/id/eprint/178961/1/WRAP-Priced-risk-corporate-bonds-23.pdf",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--references", action="store_true", help="Also cache the cited papers and source webpage")
    args = parser.parse_args()
    raw = ROOT / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / "data" / "source_manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest = dict(previous)
    for name, url in (SOURCES | REFERENCES if args.references else SOURCES).items():
        path = raw / name
        if not path.exists():
            print(f"Downloading {name}", flush=True)
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (academic research)"})
            partial = path.with_suffix(path.suffix + ".partial")
            with urllib.request.urlopen(request, timeout=120) as response, partial.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            partial.replace(path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if name in previous and digest != previous[name]["sha256"]:
            raise ValueError(f"Cached source differs from recorded hash: {name}")
        manifest[name] = {
            "url": url,
            "retrieved_utc": previous.get(name, {}).get("retrieved_utc", datetime.now(timezone.utc).isoformat()),
            "sha256": digest,
            "bytes": path.stat().st_size,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"Cached {name}: {path.stat().st_size:,} bytes", flush=True)


if __name__ == "__main__":
    main()

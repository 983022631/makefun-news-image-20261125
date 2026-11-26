"""Entry point: copy the committed front-page image to the output directory."""
import os
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    written = 0
    with src.open("rb") as fin, dst.open("wb") as fout:
        while True:
            chunk = fin.read(65536)
            if not chunk:
                break
            fout.write(chunk)
            written += len(chunk)
    if written != src.stat().st_size:
        raise SystemExit("entry.png copy incomplete")


if __name__ == "__main__":
    main()

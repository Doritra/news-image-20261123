"""News-image entry for Monday 23 November 2026.

The repository ships the finished front page as entry.png (39 stories
reported on Monday 23 November 2026: Ukraine's sinking of the Russian
corvette Merkury off Libya, the COP31 collapse in Antalya, and the
Kyiv-region strikes lead; eight sections cover Europe, the Middle
East, Africa, Asia-Pacific, the Americas, economy and technology,
science and health, and sport and culture, plus a "day in numbers"
strip). This program copies that image to the output directory,
byte for byte, with no network use. Outside the grader,
MAKEFUN_OUTPUT_DIR stands in for /output.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / "entry.png"
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    # Guard the gate: the shipped file must be a whole PNG within limits.
    data = target.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    assert len(data) <= 1_048_576, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()

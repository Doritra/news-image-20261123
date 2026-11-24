[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Doritra/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Doritra/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# News Image — Monday 23 November 2026

One image that sums up the world's news of Monday 23 November 2026.

`entry.png` is a 1024x1024 front page with 39 stories reported that
day, grouped by region and field: Ukraine's sinking of the Russian
corvette Merkury off Libya, the collapse of the COP31 climate talks in
Antalya, and the Russian strikes on the Kyiv region lead the page,
followed by sections for Europe and Ukraine, Asia-Pacific, the
Americas, the Middle East and Iran, Africa, economy and technology,
science and health, and sport and culture, plus a "day in numbers"
strip.

## Run

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

`main.py` (Python 3, standard library only, no network) copies
`entry.png` to the output directory byte for byte, so repeated runs
write identical bytes.

## Rebuild the image

`build_image.py` renders `entry.png` programmatically with Pillow
from the story lists in that file. The render is deterministic:
fixed palette, fixed fonts, no clock and no randomness. It also
fails loudly if any story line is wider than its column.

Stories were compiled on 24 November 2026 (Asia/Jakarta) from
reporting dated 23 November 2026 by AP, Reuters, AFP, Al Jazeera,
The Guardian, ESA and national outlets.

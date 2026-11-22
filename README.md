# The World in One Day — Sunday, 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/agielthree/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/agielthree/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A one-page newspaper poster summing up the world's news of Sunday,
22 November 2026: the IRGC's claimed strikes on U.S. positions in
Bahrain, the COP31 fossil-fuel deadlock in Antalya, the capture of
cartel kingpin "El Chapo Isidro" in Mexico, the drone strike on the
Russian cargo ship Sparta II, the reported hack of the FBI's NCIC
database, and the capsized boat in Bayelsa, Nigeria. All six stories
were first reported on that day.

## How it is built

`draw_poster.py` draws the 1024x1024 poster with Pillow primitives
only — no network, no randomness, no clock — so every run produces
byte-identical output. `main.ts` copies the finished `entry.png` to
the output directory the grader reads.

## Run it locally

```sh
python3 draw_poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The finished poster is `out/entry.png`.

Entry for the [make.fun bounty "Sum up 22 November's world news in one image"](https://make.fun/bounty/news-image-20261122), built by [@agielthree](https://make.fun/bounty/news-image-20261122).
